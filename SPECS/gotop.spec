%define debug_package %{nil}

%global gh_user     cjbassi
%global gh_commit   be57ff76b9f567b697c39a78115a02b3917b1fea
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})

# see https://fedoraproject.org/wiki/PackagingDrafts/Go#Build_ID
%global _dwz_low_mem_die_limit 0
%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') " -i -v -x %{?**};
%endif

Name:           gotop
Version:        2.0.1
Release:        1%{?dist}
Summary:        Another terminal based graphical activity monitor, inspired by gtop and vtop, this time written in Go!
Group:          Applications/System
License:        MIT
URL:            https://github.com/%{gh_user}/%{name}
BuildRequires:  git golang

%description
Another terminal based graphical activity monitor, inspired by gtop and vtop, this time written in Go!
See the project site for configuration options: https://github.com/cjbassi/gotop

%prep
wget https://github.com/%{gh_user}/%{name}/archive/%{version}.tar.gz
tar xzf %{version}.tar.gz
mkdir -p %{_builddir}/src/github.com/%{gh_user}/
cd %{_builddir}/src/github.com/%{gh_user}/
ln -snf %{_builddir}/%{name}-%{version} %{name}
cd %{name}

%build
export GOPATH="%{_builddir}"
export PATH=$PATH:"%{_builddir}"/bin
cd %{_builddir}/src/github.com/%{gh_user}/%{name}
export LDFLAGS="${LDFLAGS} -X main.commit=%{gh_short} -X main.date=$(date -u +%Y%m%d.%H%M%%S) -X main.version=%{version}"

%gobuild -o %{_builddir}/bin/%{name}

%install
install -Dm0755 %{_builddir}/bin/%{name} %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%doc %{name}-%{version}/LICENSE %{name}-%{version}/*.md

%changelog
* Thu Feb 7 2019 Jamie Curnow <jc@jc21.com> 2.0.1-1
- V2.0.1

* Tue Jan 22 2019 Jamie Curnow <jc@jc21.com> 2.0.0-1
- Initial Spec File


