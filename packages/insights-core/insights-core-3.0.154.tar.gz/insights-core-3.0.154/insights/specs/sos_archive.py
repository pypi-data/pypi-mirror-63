from functools import partial
from insights.specs import Specs
from insights.core.context import SosArchiveContext
from insights.core.spec_factory import simple_file, first_of, first_file, glob_file

first_file = partial(first_file, context=SosArchiveContext)
glob_file = partial(glob_file, context=SosArchiveContext)
simple_file = partial(simple_file, context=SosArchiveContext)


class SosSpecs(Specs):
    auditctl_status = simple_file("sos_commands/auditd/auditctl_-s")
    blkid = first_file(["sos_commands/block/blkid_-c_.dev.null", "sos_commands/filesys/blkid_-c_.dev.null"])
    candlepin_log = first_of([
        simple_file("/var/log/candlepin/candlepin.log"),
        simple_file("sos_commands/foreman/foreman-debug/var/log/candlepin/candlepin.log")
    ])
    candlepin_error_log = first_of([
        simple_file("var/log/candlepin/error.log"),
        simple_file(r"sos_commands/foreman/foreman-debug/var/log/candlepin/error.log")
    ])
    catalina_out = glob_file("var/log/tomcat*/catalina.out")
    catalina_server_log = glob_file("var/log/tomcat*/catalina*.log")
    ceph_osd_tree_text = simple_file("sos_commands/ceph/ceph_osd_tree")
    ceph_report = simple_file("sos_commands/ceph/ceph_report")
    ceph_health_detail = simple_file("sos_commands/ceph/ceph_health_detail_--format_json-pretty")
    chkconfig = first_file(["sos_commands/startup/chkconfig_--list", "sos_commands/services/chkconfig_--list"])
    cpupower_frequency_info = simple_file("sos_commands/processor/cpupower_frequency-info")
    date = first_of([simple_file("sos_commands/general/date"), simple_file("sos_commands/date/date")])
    df__al = first_file(["sos_commands/filesys/df_-al", "sos_commands/filesys/df_-al_-x_autofs"])
    display_java = simple_file("sos_commands/java/alternatives_--display_java")
    docker_info = simple_file("sos_commands/docker/docker_info")
    docker_list_containers = first_file(["sos_commands/docker/docker_ps_-a", "sos_commands/docker/docker_ps"])
    docker_list_images = simple_file("sos_commands/docker/docker_images")
    docker_image_inspect = glob_file("sos_commands/docker/docker_inspect_*")
    dmesg = first_file(["sos_commands/kernel/dmesg", "sos_commands/general/dmesg", "var/log/dmesg"])
    dmidecode = simple_file("sos_commands/hardware/dmidecode")
    dmsetup_info = simple_file("sos_commands/devicemapper/dmsetup_info_-c")
    dumpe2fs_h = glob_file("sos_commands/filesys/dumpe2fs_-h_*")
    ethtool = glob_file("sos_commands/networking/ethtool_*", ignore="ethtool_-.*")
    ethtool_S = glob_file("sos_commands/networking/ethtool_-S_*")
    ethtool_T = glob_file("sos_commands/networking/ethtool_-T_*")
    ethtool_a = glob_file("sos_commands/networking/ethtool_-a_*")
    ethtool_c = glob_file("sos_commands/networking/ethtool_-c_*")
    ethtool_g = glob_file("sos_commands/networking/ethtool_-g_*")
    ethtool_i = glob_file("sos_commands/networking/ethtool_-i_*")
    ethtool_k = glob_file("sos_commands/networking/ethtool_-k_*")
    fdisk_l_sos = first_of([glob_file(r"sos_commands/filesys/fdisk_-l_*"), glob_file(r"sos_commands/block/fdisk_-l_*")])
    foreman_production_log = first_of([simple_file("/var/log/foreman/production.log"), simple_file("sos_commands/foreman/foreman-debug/var/log/foreman/production.log")])
    foreman_proxy_conf = first_of([simple_file("/etc/foreman-proxy/settings.yml"), simple_file("sos_commands/foreman/foreman-debug/etc/foreman-proxy/settings.yml")])
    foreman_proxy_log = first_of([simple_file("/var/log/foreman-proxy/proxy.log"), simple_file("sos_commands/foreman/foreman-debug/var/log/foreman-proxy/proxy.log")])
    foreman_satellite_log = first_of([simple_file("/var/log/foreman-installer/satellite.log"), simple_file("sos_commands/foreman/foreman-debug/var/log/foreman-installer/satellite.log")])
    foreman_ssl_access_ssl_log = first_file(["var/log/httpd/foreman-ssl_access_ssl.log", r"sos_commands/foreman/foreman-debug/var/log/httpd/foreman-ssl_access_ssl.log"])
    hammer_ping = first_file(["sos_commands/foreman/hammer_ping", "sos_commands/foreman/foreman-debug/hammer-ping"])
    getcert_list = first_file(["sos_commands/ipa/ipa-getcert_list", "sos_commands/ipa/getcert_list"])
    gluster_v_info = simple_file("sos_commands/gluster/gluster_volume_info")
    gluster_v_status = simple_file("sos_commands/gluster/gluster_volume_status")
    gluster_peer_status = simple_file("sos_commands/gluster/gluster_peer_status")
    hostname = first_file(["sos_commands/general/hostname_-f", "sos_commands/host/hostname_-f"])
    hostname_default = first_file(["sos_commands/general/hostname", "sos_commands/host/hostname", "/etc/hostname", "hostname"])
    hostname_short = first_file(["sos_commands/general/hostname", "sos_commands/host/hostname", "/etc/hostname", "hostname"])
    httpd_M = simple_file("sos_commands/apache/apachectl_-M")
    installed_rpms = first_file(["sos_commands/rpm/package-data", "installed-rpms"])
    ip_addr = first_of([simple_file("sos_commands/networking/ip_-d_address"), simple_file("sos_commands/networking/ip_address")])
    ip_neigh_show = first_file(["sos_commands/networking/ip_-s_-s_neigh_show", "sos_commands/networking/ip_neigh_show"])
    ip_route_show_table_all = simple_file("sos_commands/networking/ip_route_show_table_all")
    ip_s_link = first_of([simple_file("sos_commands/networking/ip_-s_-d_link"), simple_file("sos_commands/networking/ip_-s_link"), simple_file("sos_commands/networking/ip_link")])
    iptables = first_file(["/etc/sysconfig/iptables", "/etc/sysconfig/iptables.save"])
    journal_since_boot = first_of([simple_file("sos_commands/logs/journalctl_--no-pager_--boot"), simple_file("sos_commands/logs/journalctl_--no-pager_--catalog_--boot")])
    locale = simple_file("sos_commands/i18n/locale")
    lsblk = first_file(["sos_commands/block/lsblk", "sos_commands/filesys/lsblk"])
    ls_boot = simple_file("sos_commands/boot/ls_-lanR_.boot")
    lscpu = simple_file("sos_commands/processor/lscpu")
    lsinitrd = simple_file("sos_commands/boot/lsinitrd")
    lsof = simple_file("sos_commands/process/lsof_-b_M_-n_-l")
    lsmod = simple_file("sos_commands/kernel/lsmod")
    lspci = first_of([
        simple_file("sos_commands/pci/lspci_-nnvv"),
        simple_file("sos_commands/pci/lspci_-nvv"),
        simple_file("sos_commands/pci/lspci")
    ])
    lsscsi = simple_file("sos_commands/scsi/lsscsi")
    ls_dev = first_file(["sos_commands/block/ls_-lanR_.dev", "sos_commands/devicemapper/ls_-lanR_.dev"])
    lvs = first_file(["sos_commands/lvm2/lvs_-a_-o_lv_tags_devices_--config_global_locking_type_0", "sos_commands/lvm2/lvs_-a_-o_devices"])
    modinfo_all = glob_file("sos_commands/kernel/modinfo_*")
    mount = simple_file("sos_commands/filesys/mount_-l")
    multipath__v4__ll = first_file(["sos_commands/multipath/multipath_-v4_-ll", "sos_commands/devicemapper/multipath_-v4_-ll"])
    netstat = first_file(["sos_commands/networking/netstat_-neopa", "sos_commands/networking/netstat_-W_-neopa", "sos_commands/networking/netstat_-T_-neopa"])
    netstat_agn = first_of([simple_file("sos_commands/networking/netstat_-agn"), simple_file("sos_commands/networking/netstat_-W_-agn"), simple_file("sos_commands/networking/netstat_-T_-agn")])
    netstat_s = simple_file("sos_commands/networking/netstat_-s")
    nmcli_dev_show = simple_file("sos_commands/networking/nmcli_device_show")
    nmcli_dev_show_sos = glob_file(["sos_commands/networking/nmcli_dev_show_*", "sos_commands/networkmanager/nmcli_dev_show_*"])
    ntptime = simple_file("sos_commands/ntp/ntptime")
    openvswitch_other_config = simple_file("sos_commands/openvswitch/ovs-vsctl_-t_5_get_Open_vSwitch_._other_config")
    ovs_vsctl_show = simple_file("sos_commands/openvswitch/ovs-vsctl_-t_5_show")
    pcs_config = simple_file("sos_commands/pacemaker/pcs_config")
    pcs_quorum_status = simple_file("sos_commands/pacemaker/pcs_quorum_status")
    pcs_status = simple_file("sos_commands/pacemaker/pcs_status")
    podman_image_inspect = glob_file("sos_commands/podman/podman_inspect_*")
    podman_list_containers = first_file(["sos_commands/podman/podman_ps_-a", "sos_commands/podman/podman_ps"])
    podman_list_images = simple_file("sos_commands/podman/podman_images")
    ps_alxwww = simple_file("sos_commands/process/ps_alxwww")
    ps_aux = first_file(["sos_commands/process/ps_aux", "sos_commands/process/ps_auxwww", "sos_commands/process/ps_auxcww"])
    ps_auxcww = first_file(["sos_commands/process/ps_auxcww", "sos_commands/process/ps_auxwww", "sos_commands/process/ps_aux"])
    ps_auxww = first_file(["sos_commands/process/ps_auxww", "sos_commands/process/ps_auxwww", "sos_commands/process/ps_aux", "sos_commands/process/ps_auxcww"])
    puppet_ssl_cert_ca_pem = first_file([
        "/etc/puppetlabs/puppet/ssl/certs/ca.pem",
        "sos_commands/foreman/foreman-debug/var/lib/puppet/ssl/certs/ca.pem"
    ])
    pvs = first_file(["sos_commands/lvm2/pvs_-a_-v_-o_pv_mda_free_pv_mda_size_pv_mda_count_pv_mda_used_count_pe_start_--config_global_locking_type_0", "sos_commands/lvm2/pvs_-a_-v", "sos_commands/devicemapper/pvs_-a_-v"])
    qpid_stat_q = first_file([
        "sos_commands/pulp/qpid-stat_-q_--ssl-certificate_.etc.pki.pulp.qpid.client.crt_-b_amqps_..localhost_5671",
        "sos_commands/pulp/qpid-stat_-q_--ssl-certificate_.etc.pki.katello.qpid_client_striped.crt_-b_amqps_..localhost_5671",
        "sos_commands/katello/qpid-stat_-q_--ssl-certificate_.etc.pki.pulp.qpid.client.crt_-b_amqps_..localhost_5671",
        "sos_commands/katello/qpid-stat_-q_--ssl-certificate_.etc.pki.katello.qpid_client_striped.crt_-b_amqps_..localhost_5671",
        "sos_commands/foreman/foreman-debug/qpid-stat-q",
        "qpid-stat-q",
        "sos_commands/foreman/foreman-debug/qpid_stat_queues",
        "qpid_stat_queues"
    ])
    qpid_stat_u = first_file([
        "sos_commands/pulp/qpid-stat_-u_--ssl-certificate_.etc.pki.pulp.qpid.client.crt_-b_amqps_..localhost_5671",
        "sos_commands/pulp/qpid-stat_-u_--ssl-certificate_.etc.pki.katello.qpid_client_striped.crt_-b_amqps_..localhost_5671",
        "sos_commands/katello/qpid-stat_-u_--ssl-certificate_.etc.pki.pulp.qpid.client.crt_-b_amqps_..localhost_5671",
        "sos_commands/katello/qpid-stat_-u_--ssl-certificate_.etc.pki.katello.qpid_client_striped.crt_-b_amqps_..localhost_5671",
        "sos_commands/foreman/foreman-debug/qpid-stat-u",
        "qpid-stat-u",
        "sos_commands/foreman/foreman-debug/qpid_stat_subscriptions",
        "qpid_stat_subscriptions"
    ])
    rabbitmq_report = simple_file("sos_commands/rabbitmq/rabbitmqctl_report")
    rabbitmq_report_of_containers = glob_file("sos_commands/rabbitmq/docker_exec_-t_rabbitmq-bundle-docker-*_rabbitmqctl_report")
    rhn_charsets = first_file(["sos_commands/satellite/rhn-charsets", "sos_commands/rhn/rhn-charsets"])
    root_crontab = first_file(["sos_commands/crontab/root_crontab", "sos_commands/cron/root_crontab"])
    route = simple_file("sos_commands/networking/route_-n")
    sestatus = simple_file("sos_commands/selinux/sestatus_-b")
    sssd_logs = glob_file("var/log/sssd/*.log")
    samba_logs = glob_file("var/log/samba/log.*")
    subscription_manager_list_consumed = first_file([
        'sos_commands/yum/subscription-manager_list_--consumed',
        'sos_commands/subscription_manager/subscription-manager_list_--consumed',
        'sos_commands/general/subscription-manager_list_--consumed']
    )
    subscription_manager_list_installed = first_file([
        'sos_commands/yum/subscription-manager_list_--installed',
        'sos_commands/subscription_manager/subscription-manager_list_--installed',
        'sos_commands/general/subscription-manager_list_--installed']
    )
    sysctl = simple_file("sos_commands/kernel/sysctl_-a")
    systemctl_list_unit_files = simple_file("sos_commands/systemd/systemctl_list-unit-files")
    systemctl_list_units = first_file(["sos_commands/systemd/systemctl_list-units", "sos_commands/systemd/systemctl_list-units_--all"])
    systemctl_show_all_services = simple_file("sos_commands/systemd/systemctl_show_service_--all")
    teamdctl_config_dump = glob_file("sos_commands/teamd/teamdctl_*_config_dump")
    teamdctl_state_dump = glob_file("sos_commands/teamd/teamdctl_*_state_dump")
    uname = simple_file("sos_commands/kernel/uname_-a")
    uptime = first_of([simple_file("sos_commands/general/uptime"), simple_file("sos_commands/host/uptime")])
    var_qemu_xml = glob_file(r"var/run/libvirt/qemu/*.xml")
    vdsm_import_log = glob_file("var/log/vdsm/import/import-*.log")
    vgdisplay = first_file(["sos_commands/lvm2/vgdisplay_-vv_--config_global_locking_type_0", "sos_commands/lvm2/vgdisplay_-vv"])
    vgs = first_file(["sos_commands/lvm2/vgs_-v_-o_vg_mda_count_vg_mda_free_vg_mda_size_vg_mda_used_count_vg_tags_--config_global_locking_type_0", "sos_commands/lvm2/vgs_-v", "sos_commands/devicemapper/vgs_-v"])
    xfs_info = glob_file("sos_commands/xfs/xfs_info*")
    yum_repolist = simple_file("sos_commands/yum/yum_-C_repolist")
