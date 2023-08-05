from datetime import datetime
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig, apps as django_apps
from django.core.checks import register
from django.core.management.color import color_style
from django_collect_offline.apps import AppConfig as BaseDjangoCollectOfflineAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
from django.db.models.signals import post_migrate
from edc_auth.group_permissions_updater import GroupPermissionsUpdater

from .system_checks import ambition_check

style = color_style()


def post_migrate_update_edc_auth(sender=None, **kwargs):
    from ambition_auth.codenames_by_group import get_codenames_by_group

    GroupPermissionsUpdater(
        codenames_by_group=get_codenames_by_group(), verbose=True, apps=django_apps
    )


class AppConfig(DjangoAppConfig):
    name = "ambition_edc"

    def ready(self):
        # from ambition_rando.system_checks import randomization_list_check
        # register(randomization_list_check)(["ambition_edc"])
        post_migrate.connect(post_migrate_update_edc_auth, sender=self)
        register(ambition_check)


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    institution = "London School of Hygiene & Tropical Medicine"
    project_name = "Ambition"
    project_repo = "https://github.com/ambition-trial"
    protocol = "BHP092"
    protocol_name = "Ambition"
    protocol_number = "092"
    protocol_title = (
        "High Dose AMBISOME on a Fluconazole Backbone for Cryptococcal Meningitis "
        "Induction Therapy in sub-Saharan Africa: A Phase 3 Randomised Controlled "
        "Non-Inferiority Trial (P.I. Joe Jarvis)."
    )
    study_open_datetime = datetime(2016, 12, 31, 0, 0, 0, tzinfo=gettz("UTC"))
    study_close_datetime = datetime(2022, 12, 31, 23, 59, 59, tzinfo=gettz("UTC"))


class EdcLabAppConfig(BaseEdcLabAppConfig):
    result_model = "edc_lab.result"


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    device_role = CENTRAL_SERVER
    device_id = "99"


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        "ambition_subject": ("subject_visit", "ambition_subject.subjectvisit")
    }


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = "092"


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {"ambition_subject.subjectvisit": "reason"}


class DjangoCollectOfflineAppConfig(BaseDjangoCollectOfflineAppConfig):
    base_template_name = "edc_dashboard/bootstrap3/base.html"
