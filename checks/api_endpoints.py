from lib.base import CheckBase, whitelist


class CheckDeprecatedAPIEndpoints(CheckBase):
    enable_parameter = "deprecated-api-endpoints"
    description = 'check that no deprecated api endpoints are used'
    default_enabled = True

    def _do_check_(self, m, apis, refs):
        template = "{} {} is using deprecated endpoint {}.  See {} for details"

        kind = m['kind']
        name = m['metadata']['name']
        version = m['apiVersion']
        ref = refs.get(version, "")
        err_msg = template.format(kind, name, version, ref)

        assert version not in apis, err_msg

    @whitelist('NetworkPolicy', 'Ingress')
    def check_deprecated_networking_endpoints(self, m):
        deprecated = ["extensions/v1beta1"]
        refs = {
            "extensions/v1beta1":
            "https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16"
        }
        self._do_check_(m, deprecated, refs)

    @whitelist('DaemonSet', 'Deployment', 'StatefulSet', 'ReplicaSet')
    def check_deprecated_apps_endpoints(self, m):
        deprecated = ["extensions/v1beta1", "apps/v1beta1", "apps/v1beta2"]
        refs = {
            "extensions/v1beta1":
            "https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16",
            "apps/v1beta1":
            "https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16",
            "apps/v1beta2":
            "https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16"
        }
        self._do_check_(m, deprecated, refs)

    @whitelist('PodSecurityPolicy')
    def check_deprecated_policy_endpoints(self, m):
        deprecated = ["extensions/v1beta1"]
        refs = {
            "extensions/v1beta1":
            "https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16"
        }
        self._do_check_(m, deprecated, refs)
