#!/usr/bin/env bash
set -euxo pipefail

echo "UPLOADING PACKAGES"

# Ubuntu
package_cloud push datawireio/stable/ubuntu/xenial  packaging/out/xenial/kubernaut_${KUBERNAUT_VERSION}_amd64.deb
package_cloud push datawireio/stable/ubuntu/yakkety packaging/out/yakkety/kubernaut_${KUBERNAUT_VERSION}_amd64.deb
package_cloud push datawireio/stable/ubuntu/zesty   packaging/out/zesty/kubernaut_${KUBERNAUT_VERSION}_amd64.deb

# Fedora
package_cloud push datawireio/stable/fedora/25 packaging/out/fedora-25/kubernaut-${KUBERNAUT_VERSION}-1.x86_64.rpm
package_cloud push datawireio/stable/fedora/26 packaging/out/fedora-26/kubernaut-${KUBERNAUT_VERSION}-1.x86_64.rpm

echo "UPLOADING PACKAGES FINISHED"
