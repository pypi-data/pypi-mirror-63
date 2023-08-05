# Copyright (c) 2020, Manfred Moitzi
# License: MIT License
from typing import TYPE_CHECKING, Iterable, cast
from ezdxf.lldxf.const import DXFStructureError, DXFTypeError
from ezdxf.query import EntityQuery
from ezdxf.math import Vector

if TYPE_CHECKING:
    from ezdxf.eztypes import Insert, BaseLayout, DXFGraphic


def explode_block_reference(block_ref: 'Insert', target_layout: 'BaseLayout') -> EntityQuery:
    """
    Explode a block reference into single DXF entities.

    Transforms the block entities into the required :ref:`WCS` location by applying the block reference
    attributes `insert`, `extrusion`, `rotation` and the scaling values `xscale`, `yscale` and `zscale`.
    Multiple inserts by row and column attributes is not supported.

    Returns an :class:`~ezdxf.query.EntityQuery` container with all exploded DXF entities.

    Args:
        block_ref: Block reference entity (:class:`~ezdxf.entities.Insert`)
        target_layout: target layout for exploded DXF entities (modelspace, paperspace or block layout),
                       if ``None`` the layout of the block reference is used.

    .. warning::

        **Non uniform scaling** lead to incorrect results for text entities (TEXT, MTEXT, ATTRIB) and
        some other entities like ELLIPSE, SHAPE, HATCH with arc or ellipse path segments and
        POLYLINE/LWPOLYLINE with arc segments.

    """
    if block_ref.doc is None or block_ref.doc.entitydb is None:
        raise DXFStructureError('Block reference has to be assigned to a DXF document.')

    entitydb = block_ref.doc.entitydb
    if entitydb is None:
        raise DXFStructureError('Exploding a block reference requires an entity database.')

    entities = []

    for entity in virtual_entities(block_ref):
        entitydb.add(entity)
        target_layout.add_entity(entity)
        entities.append(entity)

    # Process attached ATTRIB entities:
    for attrib in block_ref.attribs:
        # Attached ATTRIB entities are already located in the WCS
        target_layout.add_entity(attrib)
        entities.append(attrib)

    # Unlink attributes else they would be destroyed by deleting the block reference.
    block_ref.attribs = []
    source_layout = block_ref.get_layout()
    if source_layout is not None:
        # Remove and destroy exploded INSERT if assigned to a layout
        source_layout.delete_entity(block_ref)
    else:
        entitydb.delete_entity(block_ref)
    return EntityQuery(entities)


def virtual_entities(block_ref: 'Insert') -> Iterable['DXFGraphic']:
    """
    Yields 'virtual' entities of block reference `block_ref`. This method is meant to examine the the block reference
    entities without the need to explode the block reference.

    This entities are located at the 'exploded' positions, but are not stored in the entity database, have no handle
    are not assigned to any layout. It is possible to convert this entities into regular drawing entities, this lines
    show how to add the virtual `entity` to the entity database and assign this entity to the modelspace::

        doc.entitydb.add(entity)
        msp = doc.modelspace()
        msp.add_entity(entity)

    To explode the whole block reference use :meth:`~ezdxf.entities.Insert.explode`.

    Args:
        block_ref: Block reference entity (:class:`~ezdxf.entities.Insert`)

    .. warning::

        **Non uniform scaling** returns incorrect results for text entities (TEXT, MTEXT, ATTRIB) and
        some other entities like ELLIPSE, SHAPE, HATCH with arc or ellipse path segments and
        POLYLINE/LWPOLYLINE with arc segments.

    """
    brcs = block_ref.brcs()
    # Non uniform scaling will produce incorrect results for some entities!
    xscale = block_ref.dxf.xscale
    yscale = block_ref.dxf.yscale
    uniform_scaling = max(abs(xscale), abs(yscale))
    non_uniform_scaling = xscale != yscale

    block_layout = block_ref.block()
    if block_layout is None:
        raise DXFStructureError(f'Required block definition for "{block_ref.dxf.name}" does not exist.')

    for entity in block_layout:
        dxftype = entity.dxftype()
        if dxftype == 'ATTDEF':  # do not explode ATTDEF entities
            continue

        # Copy entity with all DXF attributes
        try:
            copy = entity.copy()
        except DXFTypeError:
            continue  # non copyable entities will be ignored

        if non_uniform_scaling and dxftype in {'ARC', 'CIRCLE'}:
            from ezdxf.entities import Ellipse
            copy = Ellipse.from_arc(entity)
            dxftype = copy.dxftype()

        # Basic transformation from BRCS to WCS
        try:
            copy.transform_to_wcs(brcs)
        except NotImplementedError:  # entities without 'transform_to_ucs' support will be ignored
            continue

        # Apply DXF attribute scaling:
        # 1. simple entities without properties to scale
        if dxftype in {'LINE', 'POINT', 'LWPOLYLINE', 'POLYLINE', 'MESH', 'HATCH', 'SPLINE',
                       'SOLID', '3DFACE', 'TRACE', 'IMAGE', 'WIPEOUT', 'XLINE', 'RAY', 'LIGHT', 'HELIX'}:
            pass  # nothing else to do
        elif dxftype in {'CIRCLE', 'ARC'}:
            # simple uniform scaling of radius
            # How to handle non uniform scaling? -> Ellipse
            copy.dxf.radius = entity.dxf.radius * uniform_scaling
        elif dxftype == 'ELLIPSE':
            if non_uniform_scaling:
                # ELLIPSE -> ELLIPSE
                if entity.dxftype() == 'ELLIPSE':
                    ellipse = cast('Ellipse', entity)
                    major_axis = Vector(ellipse.dxf.major_axis)
                    minor_axis = ellipse.minor_axis
                    major_axis_length = brcs.direction_to_wcs(major_axis).magnitude
                    minor_axis_length = brcs.direction_to_wcs(minor_axis).magnitude
                    copy.dxf.ratio = max(minor_axis_length / major_axis_length, 1e-6)
                else:  # ARC -> ELLIPSE
                    scale = max(min((yscale / xscale), 1.0), 1e-6)
                    copy.dxf.ratio = scale
        elif dxftype == 'MTEXT':
            # Scale MTEXT height/width just by uniform_scaling, how to handle non uniform scaling?
            copy.dxf.char_height *= uniform_scaling
            copy.dxf.width *= uniform_scaling
        elif dxftype in {'TEXT', 'ATTRIB'}:
            # Scale TEXT height just by uniform_scaling, how to handle non uniform scaling?
            copy.dxf.height *= uniform_scaling
        elif dxftype == 'INSERT':
            # Set scaling of child INSERT to scaling of parent INSERT
            for scale in ('xscale', 'yscale', 'zscale'):
                if block_ref.dxf.hasattr(scale):
                    original_scale = copy.dxf.get_default(scale)
                    block_ref_scale = block_ref.dxf.get(scale)
                    copy.dxf.set(scale, original_scale * block_ref_scale)
            if uniform_scaling != 1:
                # Scale attached ATTRIB entities:
                # Scale height just by uniform_scaling, how to handle non uniform scaling?
                for attrib in copy.attribs:
                    attrib.dxf.height *= uniform_scaling
        elif dxftype == 'SHAPE':
            # Scale SHAPE size just by uniform_scaling, how to handle non uniform scaling?
            copy.dxf.size *= uniform_scaling
        else:  # unsupported entity will be ignored
            continue
        yield copy
