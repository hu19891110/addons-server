from rest_framework import serializers

from olympia.addons.models import Addon
from olympia.addons.serializers import AddonSerializer, VersionSerializer
from olympia.amo.helpers import absolutify
from olympia.versions.models import Version


class DiscoveryVersionSerializer(VersionSerializer):
    class Meta:
        fields = ('compatibility', 'files',)
        model = Version


class DiscoveryAddonSerializer(AddonSerializer):
    current_version = DiscoveryVersionSerializer()

    class Meta:
        fields = ('id', 'current_version', 'guid', 'icon_url', 'name',
                  'slug', 'theme_data', 'type', 'url',)
        model = Addon


class DiscoverySerializer(serializers.Serializer):
    heading = serializers.CharField()
    description = serializers.CharField()
    addon = DiscoveryAddonSerializer()

    def to_representation(self, instance):
        data = super(DiscoverySerializer, self).to_representation(instance)
        # Note: target and rel attrs are added in addons-frontend.
        addon_link = '<a href="{0}">{1}</a>'.format(
            absolutify(instance.addon.get_url_path()),
            unicode(instance.addon.name))

        if data['heading'] is None:
            data['heading'] = addon_link
        else:
            data['heading'] = data['heading'].replace(
                '{start_sub_heading}', '<span>').replace(
                '{end_sub_heading}', '</span>').replace(
                '{addon_name}', addon_link)
        return data
