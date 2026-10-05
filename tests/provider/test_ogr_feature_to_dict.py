# AI generated code: Junie claude-opus-5-5
"""Tests for the fast OGR feature serializer."""

from osgeo import ogr

from pygeoapi.provider.ogr import _feature_to_dict


def make_layer():
    """Create an in-memory OGR layer with a string and an integer field."""
    ds = ogr.GetDriverByName('MEM').CreateDataSource('mem')
    layer = ds.CreateLayer('test', geom_type=ogr.wkbPoint)
    layer.CreateField(ogr.FieldDefn('name', ogr.OFTString))
    layer.CreateField(ogr.FieldDefn('count', ogr.OFTInteger))
    return ds, layer


def test_feature_to_dict_matches_export_to_json():
    """Test that the serializer yields the same output as ExportToJson"""
    ds, layer = make_layer()
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField('name', 'a')
    feature.SetGeometry(ogr.CreateGeometryFromWkt('POINT (1 2)'))
    layer.CreateFeature(feature)
    feature = layer.GetFeature(feature.GetFID())

    expected = feature.ExportToJson(as_object=True)
    result = _feature_to_dict(feature, feature.GetGeometryRef())

    assert result == expected
    assert result['properties'] == {'name': 'a', 'count': None}


def test_feature_to_dict_without_geometry():
    """Test that features without geometry serialize to a null geometry"""
    ds, layer = make_layer()
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField('count', 3)

    result = _feature_to_dict(feature, None)

    assert result['geometry'] is None
    assert result['properties'] == {'name': None, 'count': 3}
