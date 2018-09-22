# -*- coding: utf-8 -*-


from base import BaseResponse


class GeokretResponse(BaseResponse):

    @property
    def name(self):
        return self.get_attribute('name')

    @property
    def description(self):
        return self.get_attribute('description')

    @property
    def holder(self):
        return self.get_attribute('holder')

    @property
    def missing(self):
        return self.get_attribute('missing')

    @property
    def distance(self):
        return self.get_attribute('distance')

    @property
    def caches_count(self):
        return self.get_attribute('caches-count')

    @property
    def pictures_count(self):
        return self.get_attribute('pictures-count')

    @property
    def average_rating(self):
        return self.get_attribute('average-rating')

    @property
    def type(self):
        return self['relationships']['type']['data']['id']

    @property
    def owner(self):
        return self['relationships']['owner']['data']['id']

    def assertHasTrackingCode(self, tracking_code):
        self.assertHasAttribute('tracking-code', tracking_code)

    def assertHasRelationshipOwner(self):
        self.assertHasRelationshipSelf('owner', '/v1/geokrety/%s/relationships/owner' % self.id)
        self.assertHasRelationshipRelated('owner', '/v1/geokrety/%s/owner' % self.id)

    def assertHasRelationshipHolder(self):
        self.assertHasRelationshipSelf('holder', '/v1/geokrety/%s/relationships/holder' % self.id)
        self.assertHasRelationshipRelated('holder', '/v1/geokrety/%s/holder' % self.id)

    def assertHasRelationshipGeokretyType(self):
        self.assertHasRelationshipSelf('type', '/v1/geokrety/%s/relationships/type' % self.id)
        self.assertHasRelationshipRelated('type', '/v1/geokrety/%s/type' % self.id)

    def assertHasRelationshipMoves(self):
        self.assertHasRelationshipSelf('moves', '/v1/geokrety/%s/relationships/moves' % (self.id))
        self.assertHasRelationshipRelated('moves', '/v1/geokrety/%s/moves' % (self.id))

    def assertHasRelationshipOwnerData(self, user_id):
        self.assertHasRelationshipData('owner', user_id, 'user')

    def assertHasRelationshipHolderData(self, user_id):
        self.assertHasRelationshipData('holder', user_id, 'user')

    def assertHasRelationshipGeokretyTypeData(self, user_id):
        self.assertHasRelationshipData('type', user_id, 'type')

    def assertHasRelationshipMovesData(self, moves_ids):
        self.assertHasRelationshipDatas('moves', moves_ids, 'move')

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('name', obj.name)
        self.assertHasAttribute('description', obj.description)
        self.assertHasAttribute('missing', obj.missing)
        # self.assertHasAttribute('archived', obj.archived)  # TODO
        self.assertHasAttribute('distance', obj.distance)
        self.assertHasAttribute('caches-count', obj.caches_count)
        self.assertHasAttribute('pictures-count', obj.pictures_count)
        self.assertHasAttribute('average-rating', obj.average_rating)
        # self.assertHasAttribute('country-track', obj.country_track)  # TODO
        self.assertHasRelationshipOwner()
        self.assertHasRelationshipHolder()
        self.assertHasRelationshipMoves()
        self.assertHasRelationshipGeokretyType()
        self.assertHasRelationshipGeokretyTypeData(obj.type)
