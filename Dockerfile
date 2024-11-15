FROM ubuntu:22.04 AS rtubuntu

RUN apt-get update && \
    apt-get install -y --no-install-recommends rt-tests && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


FROM debian:bookworm-slim

# Copy rt-tests binaries individually
RUN apt-get update && \
    apt-get install -y --no-install-recommends libnuma1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=rtubuntu /usr/bin/cyclictest /usr/bin/cyclictest
COPY --from=rtubuntu /usr/bin/svsematest /usr/bin/svsematest
COPY --from=rtubuntu /usr/bin/pmqtest /usr/bin/pmqtest
COPY --from=rtubuntu /usr/bin/signaltest /usr/bin/signaltest
COPY --from=rtubuntu /usr/bin/sigwaittest /usr/bin/sigwaittest
COPY --from=rtubuntu /usr/bin/ptsematest /usr/bin/ptsematest
COPY --from=rtubuntu /usr/bin/cyclicdeadline /usr/bin/cyclicdeadline
COPY --from=rtubuntu /usr/bin/deadline_test /usr/bin/deadline_test
COPY --from=rtubuntu /usr/bin/hackbench /usr/bin/hackbench
COPY --from=rtubuntu /usr/bin/pip_stress /usr/bin/pip_stress
COPY --from=rtubuntu /usr/bin/pi_stress /usr/bin/pi_stress
COPY --from=rtubuntu /usr/bin/queuelat /usr/bin/queuelat
COPY --from=rtubuntu /usr/bin/rt-migrate-test /usr/bin/rt-migrate-test
WORKDIR /usr/bin
