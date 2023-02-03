from graphene import ObjectType, Schema, Argument,String,ID,Field,List,InputObjectType,Int,JSONString,Scalar

class LocationType(Scalar):
    """ Eine Klasse die einen LocationType repräsentiert"""
    pass

class MeldungType(ObjectType):
    """ Eine Klasse die eine Meldung repräsentiert"""
    meldungId = ID()
    place = String()
    lon = String()
    lat = String()
    category = String()
    auspraegung = String()
    location = LocationType()

