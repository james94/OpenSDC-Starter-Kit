FROM sdc_apt

# COPY etc-profile-d/ /opt/open_sdc/etc-profile-d

# COPY open_sdc-setup /opt/open_sdc/open_sdc-setup

RUN mkdir -p /opt/open_sdc/sdc-entries/entrypoint-func /opt/open_sdc/sdc-entries/entrypoint-main

ENV SHELL /usr/bin/bash

COPY sdc_pyentrypoint/ /opt/open_sdc/sdc-entries/sdc_pyentrypoint
 
# Add shell script fragments into these two directories to combine entrypoints

# COPY func/* /opt/open_sdc/sdc-entries/entrypoint-func/
# COPY main/* /opt/open_sdc/sdc-entries/entrypoint-main/

# Allow for homedir mount to trigger non-root user and group creation
ADD sudoers /etc

ENTRYPOINT ["python3", "-u", "/opt/open_sdc/sdc-entries/sdc_pyentrypoint/entrypoint.py"]

