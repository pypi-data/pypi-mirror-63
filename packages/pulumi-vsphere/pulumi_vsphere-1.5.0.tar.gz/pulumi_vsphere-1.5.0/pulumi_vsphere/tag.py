# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class Tag(pulumi.CustomResource):
    category_id: pulumi.Output[str]
    """
    The unique identifier of the parent category in
    which this tag will be created. Forces a new resource if changed.
    """
    description: pulumi.Output[str]
    """
    A description for the tag.
    """
    name: pulumi.Output[str]
    """
    The display name of the tag. The name must be unique
    within its category.
    """
    def __init__(__self__, resource_name, opts=None, category_id=None, description=None, name=None, __props__=None, __name__=None, __opts__=None):
        """
        The `.Tag` resource can be used to create and manage tags, which allow
        you to attach metadata to objects in the vSphere inventory to make these
        objects more sortable and searchable.
        
        For more information about tags, click [here][ext-tags-general].
        
        [ext-tags-general]: https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.vcenterhost.doc/GUID-E8E854DD-AA97-4E0C-8419-CE84F93C4058.html
        
        > **NOTE:** Tagging support is unsupported on direct ESXi connections and
        requires vCenter 6.0 or higher.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] category_id: The unique identifier of the parent category in
               which this tag will be created. Forces a new resource if changed.
        :param pulumi.Input[str] description: A description for the tag.
        :param pulumi.Input[str] name: The display name of the tag. The name must be unique
               within its category.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vsphere/blob/master/website/docs/r/tag.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if category_id is None:
                raise TypeError("Missing required property 'category_id'")
            __props__['category_id'] = category_id
            __props__['description'] = description
            __props__['name'] = name
        super(Tag, __self__).__init__(
            'vsphere:index/tag:Tag',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, category_id=None, description=None, name=None):
        """
        Get an existing Tag resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] category_id: The unique identifier of the parent category in
               which this tag will be created. Forces a new resource if changed.
        :param pulumi.Input[str] description: A description for the tag.
        :param pulumi.Input[str] name: The display name of the tag. The name must be unique
               within its category.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vsphere/blob/master/website/docs/r/tag.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["category_id"] = category_id
        __props__["description"] = description
        __props__["name"] = name
        return Tag(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

