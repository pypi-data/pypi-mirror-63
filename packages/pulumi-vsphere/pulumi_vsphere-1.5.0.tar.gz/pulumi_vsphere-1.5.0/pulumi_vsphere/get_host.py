# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetHostResult:
    """
    A collection of values returned by getHost.
    """
    def __init__(__self__, datacenter_id=None, name=None, resource_pool_id=None, id=None):
        if datacenter_id and not isinstance(datacenter_id, str):
            raise TypeError("Expected argument 'datacenter_id' to be a str")
        __self__.datacenter_id = datacenter_id
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if resource_pool_id and not isinstance(resource_pool_id, str):
            raise TypeError("Expected argument 'resource_pool_id' to be a str")
        __self__.resource_pool_id = resource_pool_id
        """
        The [managed object ID][docs-about-morefs] of the host's
        root resource pool.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetHostResult(GetHostResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHostResult(
            datacenter_id=self.datacenter_id,
            name=self.name,
            resource_pool_id=self.resource_pool_id,
            id=self.id)

def get_host(datacenter_id=None,name=None,opts=None):
    """
    The `.Host` data source can be used to discover the ID of a vSphere
    host. This can then be used with resources or data sources that require a host
    managed object reference ID.
    
    :param str datacenter_id: The [managed object reference
           ID][docs-about-morefs] of a datacenter.
    :param str name: The name of the host. This can be a name or path. Can be
           omitted if there is only one host in your inventory.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-vsphere/blob/master/website/docs/d/host.html.markdown.
    """
    __args__ = dict()

    __args__['datacenterId'] = datacenter_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('vsphere:index/getHost:getHost', __args__, opts=opts).value

    return AwaitableGetHostResult(
        datacenter_id=__ret__.get('datacenterId'),
        name=__ret__.get('name'),
        resource_pool_id=__ret__.get('resourcePoolId'),
        id=__ret__.get('id'))
