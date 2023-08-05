# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetTagResult:
    """
    A collection of values returned by getTag.
    """
    def __init__(__self__, category_id=None, description=None, name=None, id=None):
        if category_id and not isinstance(category_id, str):
            raise TypeError("Expected argument 'category_id' to be a str")
        __self__.category_id = category_id
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetTagResult(GetTagResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTagResult(
            category_id=self.category_id,
            description=self.description,
            name=self.name,
            id=self.id)

def get_tag(category_id=None,name=None,opts=None):
    """
    Use this data source to access information about an existing resource.
    
    :param str category_id: The ID of the tag category the tag is located in.
    :param str name: The name of the tag.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-vsphere/blob/master/website/docs/d/tag.html.markdown.
    """
    __args__ = dict()

    __args__['categoryId'] = category_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('vsphere:index/getTag:getTag', __args__, opts=opts).value

    return AwaitableGetTagResult(
        category_id=__ret__.get('categoryId'),
        description=__ret__.get('description'),
        name=__ret__.get('name'),
        id=__ret__.get('id'))
