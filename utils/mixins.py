# coding=utf-8
from __future__ import unicode_literals
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext as _


class CreateMixin(object):
    def createMixin(self, validated_data):
        api_view = self.context.get('view')
        obj = self.Meta.model.objects.create(**validated_data)
        return obj

    def get_request(self):
        api_view = self.context.get('view')
        return api_view.request if hasattr(api_view, 'request') else None


class ParameterCheckMixin(object):
    def check_float_param(self, param_name, required=True, post=True):
        p = self.request.data.get(param_name) if post else self.request.query_params.get(param_name)
        if not p:
            if required:
                raise ValidationError(_('缺少参数 %(param)s ') % {'param': param_name})
            else:
                return None
        try:
            p = float(p)
        except:
            raise ValidationError(_('参数格式错误 %(param)s ') % {'param': param_name})
        return p

    def check_int_param(self, param_name, required=True, post=True):
        p = self.request.data.get(param_name) if post else self.request.query_params.get(param_name)
        if not p:
            if required:
                raise ValidationError(_('缺少参数 %(param)s ') % {'param': param_name})
            else:
                return None
        try:
            p = int(p)
        except:
            raise ValidationError(_('参数格式错误 %(param)s ') % {'param': param_name})
        return p

    def check_int_list_param(self, param_name, required=True, post=True):
        p = self.request.data.get(param_name) if post else self.request.query_params.get(param_name)
        if not p:
            if required:
                raise ValidationError(_('缺少参数 %(param)s ') % {'param': param_name})
            else:
                return []
        try:
            p = map(lambda x: int(x), p)
        except:
            raise ValidationError(_('参数格式错误 %(param)s ') % {'param': param_name})
        return p

    def check_str_param(self, param_name, required=True, post=True):
        p = self.request.data.get(param_name) if post else self.request.query_params.get(param_name)
        if not p:
            if required:
                raise ValidationError(_('缺少参数 %(param)s ') % {'param': param_name})
            else:
                return None
        return p

    def check_location_param(self, required=True, post=True, use_string=False):
        if use_string:
            lat = self.check_str_param('lat', required=required, post=post)
            lon = self.check_str_param('lon', required=required, post=post)
        else:
            lat = self.check_float_param('lat', required=required, post=post)
            lon = self.check_float_param('lon', required=required, post=post)
        if lat is None or lon is None:
            return None
        return {
            "latitude": lat,
            "longitude": lon
        }

    def check_list_param(self, param_name, required=True, post=True, valid_type=None):
        p = self.request.data.get(param_name) if post else self.request.query_params.get(param_name)
        if not p:
            if required:
                raise ValidationError(_('缺少参数 %(param)s ') % {'param': param_name})
            else:
                return None
        if isinstance(p, list):
            res = list()
            try:
                for item in p:
                    if valid_type:
                        res.append(valid_type(item))
                    else:
                        res.append(item)
            except:
                raise ValidationError(_('参数格式错误 %(param)s ') % {'param': param_name})
            return res
        else:
            try:
                res = list()
                if valid_type:
                    res.append(valid_type(p))
                else:
                    res.append(p)
                return res
            except:
                raise ValidationError(_('参数格式错误 %(param)s ') % {'param': param_name})
