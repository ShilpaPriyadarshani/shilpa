*** Settings ***
Library                SSHLibrary
Library                BuiltIn
Resource               config.txt

*** Keywords ***
Open Connection And Log In
    Open Connection    ${HOST}
    Login    ${USER}    ${PASSWORD}
    Write    xlogin -y
    Read Until    Password:
    Write    qnapsupport

Check disk Utility
    Write    disk status
    ${output}=    Read    delay=10s
    [return]    ${output}

create pool
    Run keyword if    "${pool_type}" == "stripe" and "${req_disk}" < "1"
    ...    Log To Console    ERROR: NEED MINIMUM ONE DISK TO CREATE A STRIPE TYPE POOL
    ...    ELSE IF    "${pool_type}" == "mirror" and "${req_disk}" < "2"
    ...    Log To Console    ERROR: NEED MINIMUM TWO DISK TO CREATE A MIRROR TYPE POOL
    ...    ELSE IF    "${pool_type}" == "triple" and "${req_disk}" < "3"
    ...    Log To Console    ERROR: NEED MINIMUM THREE DISK TO CREATE A TRIPLE TYPE POOL
    ...    ELSE IF    "${pool_type}" == "raidz1" and "${req_disk}" < "4"
    ...    Log To Console    ERROR: NEED MINIMUM FOUR DISK TO CREATE A RAIDZ1 TYPE POOL
    ...    ELSE IF    "${pool_type}" == "raidz2" and "${req_disk}" < "5"
    ...    Log To Console    ERROR: NEED MINIMUM FIVE DISK TO CREATE A RAIDZ2 TYPE POOL
    ...    ELSE IF    "${pool_type}" == "raidz3" and "${req_disk}" < "6"
    ...    Log To Console    ERROR: NEED MINIMUM SIX DISK TO CREATE A RAIDZ3 TYPE POOL
    ...    ELSE IF    "${pool_threshold}" != "${None}" and "${pool_owner}" != "${None}"
    ...    write    pool create ${pool_type} -o threshold=${pool_threshold} -o owner=${pool_owner} ${pool_name} ${Disks}
    ...    ELSE IF    "${pool_owner}" != "${None}"
    ...    write    pool create ${pool_type} -o owner=${pool_owner} ${pool_name} ${Disks}
    ...    ELSE IF    "${pool_threshold}" != "${None}"
    ...    write    pool create ${pool_type} -o threshold=${pool_threshold} ${pool_name} ${Disks}
    ...    ELSE 
    ...    write    pool create ${pool_type} ${pool_name} ${Disks}
    ${output1}=    Read    delay=30s
    ${contains}=  Evaluate   "Success" in """${output1}"""
    Run keyword if    "${contains}" == "True"
    ...    Log To Console    pool creation success
    ...    ELSE
    ...    Log To Console    error: ${output1}
    ...    [return]    ${contains}
    write    pool status
    ${output2}=    Read    delay=15s
    Should Contain    ${output2}    ${pool_name}
    [return]    ${output2}

create lun
    Run keyword if    "${encryption_value}" == "on"
    ...    write    lun create -o ${lun_property}=${lun_property_value} --encryption=${lun_encryption_value} --password={lun_password} --password-save=${lun_password_saver} ${lun_name} ${pool_name} ${lun_size}
    ...    ELSE IF    "${lun_property}" != "${None}"
    ...    write    lun create -o ${lun_property}=${lun_property_value} ${lun_name} ${pool_name} ${lun_size}
    ...    ELSE
    ...    write    lun create ${lun_name} ${pool_name} ${lun_size}
    ${output1}=    Read    delay=15s  
    Log To Console    ${output1}
    ${contains}=  Evaluate   "Success" in """${output1}"""
    write    lun status
    ${output2}=    Read    delay=15s
    Should Contain    ${output2}    ${lun_name}
    Run keyword if    "${contains}" == "True"
    ...    Log To Console    lun creation success
    ...    ELSE
    ...    Log To Console    error: ${output1}
    ...    [return]    ${contains}
    [return]    ${output2}

create Share
    Run keyword if    "${encryption_value}" == "on"
    ...    write    share create -o ${share_property}=${share_property_value} --encryption=${share_encryption_value} --password={share_password} --password-save=${share_password_saver} ${share_name} ${pool_name} ${share_size}
    ...    ELSE IF    "${lun_property}" != "${None}"
    ...    write    share create -o ${share_property}=${share_property_value} ${share_name} ${pool_name} ${share_size}
    ...    ELSE
    ...    write    share create ${share_name} ${pool_name} ${share_size}
    ${output1}=    Read    delay=15s  
    Log To Console    ${output1}
    ${contains}=  Evaluate   "Success" in """${output1}"""
    write    share status
    ${output2}=    Read    delay=15s
    Should Contain    ${output2}    ${share_name}
    Run keyword if    "${contains}" == "True"
    ...    Log To Console    share creation success
    ...    ELSE
    ...    Log To Console    error: ${output1}
    ...    [return]    ${contains}
    [return]    ${output2}

delete lun
    write    lun delete -r ${lun_name}
    ${output}=    Read    delay=60s
    [return]    ${output}

delete share
    write    share delete -r ${lun_name}
    ${output}=    Read    delay=60s
    [return]    ${output}

delete pool
    write    pool delete ${pool_name}
    ${output}=    Read    delay=20s
    [return]    ${output}

