# -*- coding: utf-8 -*-
# (c) 2013-2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from fabric.api import run, env, task
"""
from c1.maintenance.provisioning.service import service_restart, service_stopstart, service_add
from c1.maintenance.provisioning.ssh import ssh_copy_pubkeys
from c1.maintenance.provisioning.yum import yum_attach, yum_detach, yum_install, yum_downgrade, yum_attach_repo
from c1.maintenance.provisioning.apt import apt_install, apt_attach_repo
from c1.maintenance.packaging.composite import rpm_build_and_release, rpm_upload_and_release, deb_build_and_release, deb_upload_and_release, egg_build_and_release, egg_upload_and_release
from c1.maintenance.packaging.release import rpm_sign, rpm_publish, deb_publish, apt_reindex, package_push
from c1.maintenance.packaging.upload import file_upload
from c1.maintenance.provisioning.mongod import rhel_mongod_setup
from c1.maintenance.provisioning.mongod_debian import debian_mongod_setup
from c1.maintenance.provisioning.mongod import replicaset_status, upload_sysctl_settings as mongodb_upload_sysctl_settings
from c1.maintenance.provisioning.limits import node_limits
from c1.maintenance.provisioning.ngrep import install_ngrep
from c1.maintenance.administration.monitoring import logwatch, logwatch_mongod, logwatch_rem_persistence, service_version
from c1.maintenance.administration.control import probe_status_show, probe_status_set
from c1.maintenance.administration.misc import cpu_count, uname
from c1.maintenance.provisioning.ganglia import ganglia_node_setup, restart_gmond
from c1.maintenance.provisioning.boreus.netmodo import filesystem_integrity_update
from c1.maintenance.provisioning.boreus.yum import yum_proxy_add
from c1.maintenance.provisioning.config import config_modify
from c1.maintenance.roles import ansible_hosts_from_fabric_roles
from engine_release import consistency_check
"""
from elmyra.maintenance.packaging.composite import egg_build_and_release, egg_upload_and_release, deb_build_and_release
from elmyra.maintenance.roles import infrastructure

env.use_ssh_config = True
env.forward_agent = True

env.roledefs.update(infrastructure.roledefs)
"""
env.roledefs.update(mm.roledefs)
env.roledefs.update(rem.roledefs)
env.roledefs.update(tam.roledefs)
env.roledefs.update(sz.roledefs)
env.roledefs.update(vpc.roledefs)
"""


# the designated egg repository location on almera
env.eggrepo = '/srv/repository/elmyra/kotori/python-eggs'
