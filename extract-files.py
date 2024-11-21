#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/sdm660-common',
    'hardware/qcom-caf/msm8998',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/data-ipa-cfg-mgr-legacy-um',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.ant@1.0',
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.hardware.fm@1.0',
        'vendor.qti.imsrtpservice@2.0',
        'vendor.qti.imsrtpservice@2.1',
    ): lib_fixup_vendor_suffix,
    (
        'libOmxCore',
        'libdrmutils',
        'libgps.utils',
        'libllvd_smore',
        'libloc_core',
        'liblocation_api',
        'libril',
        'libsdmutils',
        'libwifi-hal-ctrl',
        'libwpa_client',
    ): lib_fixup_remove,
}


blob_fixups: blob_fixups_user_type = {
    (
        'system_ext/etc/init/dpmd.rc'
    ): blob_fixup()
        .regex_replace('/system/product/bin/', '/system/system_ext/bin/'),
    (
        'system_ext/etc/permissions/com.qti.dpmframework.xml',
        'system_ext/etc/permissions/dpmapi.xml',
    ): blob_fixup()
        .regex_replace('/system/product/framework/', '/system/system_ext/framework/'),
    (
        'system_ext/etc/permissions/qcrilhook.xml',
    ): blob_fixup()
        .regex_replace('/product/framework/qcrilhook.jar', '/system_ext/framework/qcrilhook.jar'),
    (
        'system_ext/lib64/libdpmframework.so',
    ): blob_fixup()
        .add_needed('libcutils_shim.so'),
    (
        'vendor/bin/mlipayd@1.1',
    ): blob_fixup()
        .remove_needed('vendor.xiaomi.hardware.mtdservice@1.0.so'),
    (
        'vendor/lib64/libmlipay.so',
        'vendor/lib64/libmlipay@1.1.so',
    ): blob_fixup()
        .remove_needed('vendor.xiaomi.hardware.mtdservice@1.0.so')
        .binary_regex_replace(b'/system/etc/firmware', b'/vendor/firmware\x00\x00\x00\x00'),
    (
        'vendor/bin/pm-service',
    ): blob_fixup()
        .add_needed('libutils-v33.so'),
    (
        'vendor/lib/vendor.qti.hardware.fingerprint@1.0.so',
        'vendor/lib64/vendor.qti.hardware.fingerprint@1.0.so',
    ): blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
    (
        'vendor/lib64/libwvhidl.so',
    ): blob_fixup()
        .add_needed('libcrypto_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sdm660-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
