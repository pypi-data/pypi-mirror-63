# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class Folder(pulumi.CustomResource):
    custom_attributes: pulumi.Output[dict]
    """
    Map of custom attribute ids to attribute 
    value strings to set for folder. See [here][docs-setting-custom-attributes]
    for a reference on how to set values for custom attributes.
    """
    datacenter_id: pulumi.Output[str]
    """
    The ID of the datacenter the folder will be created in.
    Required for all folder types except for datacenter folders. Forces a new
    resource if changed.
    """
    path: pulumi.Output[str]
    tags: pulumi.Output[list]
    """
    The IDs of any tags to attach to this resource. See
    [here][docs-applying-tags] for a reference on how to apply tags.
    """
    type: pulumi.Output[str]
    """
    The type of folder to create. Allowed options are
    `datacenter` for datacenter folders, `host` for host and cluster folders,
    `vm` for virtual machine folders, `datastore` for datastore folders, and
    `network` for network folders. Forces a new resource if changed.
    """
    def __init__(__self__, resource_name, opts=None, custom_attributes=None, datacenter_id=None, path=None, tags=None, type=None, __props__=None, __name__=None, __opts__=None):
        """
        The `.Folder` resource can be used to manage vSphere inventory folders.
        The resource supports creating folders of the 5 major types - datacenter
        folders, host and cluster folders, virtual machine folders, datastore folders,
        and network folders.
        
        Paths are always relative to the specific type of folder you are creating.
        Subfolders are discovered by parsing the relative path specified in `path`, so
        `foo/bar` will create a folder named `bar` in the parent folder `foo`, as long
        as that folder exists.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] custom_attributes: Map of custom attribute ids to attribute 
               value strings to set for folder. See [here][docs-setting-custom-attributes]
               for a reference on how to set values for custom attributes.
        :param pulumi.Input[str] datacenter_id: The ID of the datacenter the folder will be created in.
               Required for all folder types except for datacenter folders. Forces a new
               resource if changed.
        :param pulumi.Input[list] tags: The IDs of any tags to attach to this resource. See
               [here][docs-applying-tags] for a reference on how to apply tags.
        :param pulumi.Input[str] type: The type of folder to create. Allowed options are
               `datacenter` for datacenter folders, `host` for host and cluster folders,
               `vm` for virtual machine folders, `datastore` for datastore folders, and
               `network` for network folders. Forces a new resource if changed.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vsphere/blob/master/website/docs/r/folder.html.markdown.
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

            __props__['custom_attributes'] = custom_attributes
            __props__['datacenter_id'] = datacenter_id
            if path is None:
                raise TypeError("Missing required property 'path'")
            __props__['path'] = path
            __props__['tags'] = tags
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
        super(Folder, __self__).__init__(
            'vsphere:index/folder:Folder',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, custom_attributes=None, datacenter_id=None, path=None, tags=None, type=None):
        """
        Get an existing Folder resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] custom_attributes: Map of custom attribute ids to attribute 
               value strings to set for folder. See [here][docs-setting-custom-attributes]
               for a reference on how to set values for custom attributes.
        :param pulumi.Input[str] datacenter_id: The ID of the datacenter the folder will be created in.
               Required for all folder types except for datacenter folders. Forces a new
               resource if changed.
        :param pulumi.Input[list] tags: The IDs of any tags to attach to this resource. See
               [here][docs-applying-tags] for a reference on how to apply tags.
        :param pulumi.Input[str] type: The type of folder to create. Allowed options are
               `datacenter` for datacenter folders, `host` for host and cluster folders,
               `vm` for virtual machine folders, `datastore` for datastore folders, and
               `network` for network folders. Forces a new resource if changed.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vsphere/blob/master/website/docs/r/folder.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["custom_attributes"] = custom_attributes
        __props__["datacenter_id"] = datacenter_id
        __props__["path"] = path
        __props__["tags"] = tags
        __props__["type"] = type
        return Folder(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

