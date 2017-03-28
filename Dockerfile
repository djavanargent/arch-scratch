FROM scratch
MAINTAINER djavanargent

ADD bootstrap.tar.gz /

RUN \
  ln -sf /usr/share/zoneinfo/US/Eastern /etc/localtime && \
  pacman-key --init && \
  pacman-key --populate archlinux && \
  pacman -U --noconfirm --noprogressbar --arch x86_64 https://www.archlinux.org/packages/core/x86_64/sed/download/ && \
  sed -i "s/^Architecture = auto$/Architecture = x86_64/" /etc/pacman.conf && \
  sed -n 's/^#Server = https/Server = https/p' /etc/pacman.d/mirrorlist > /tmp/mirrorlist && \
  rankmirrors -n 3 /tmp/mirrorlist | tee /etc/pacman.d/mirrorlist && \
  rm /tmp/mirrorlist && \
  pacman -Syu --noconfirm --noprogressbar --quiet --force gzip awk && \
  paccache -r -k0 && \
  echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen && \
  locale-gen && \
  echo 'LANG=en_US.UTF-8' > /etc/locale.conf

ENV \
  LANG en_US.UTF-8

