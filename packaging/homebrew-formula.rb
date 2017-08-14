# This script is generated automatically by the release automation code in the
# Kubernaut repository:
class Kubernaut < Formula
  desc "Local development environment attached to a remote Kubernetes cluster"
  homepage "https://github.com/datawire/kubernaut"
  url "https://github.com/datawire/kubernaut/archive/__NEW_VERSION__.tar.gz"
  sha256 "__TARBALL_HASH__"

  depends_on "python3"

  def install
    bin.install "cli/telepresence"
  end

  test do
    system "telepresence", "--help"
  end
end