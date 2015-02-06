# extracted from sip.h, SIP_API_MAJOR_NR SIP_API_MINOR_NR defines
%define sip_api_major 11
%define sip_api_minor 1
%define sip_api       %{sip_api_major}.%{sip_api_minor}

Name:		python3-sip
Summary:	Riverbanks's python sip
Version:	4.16.1
Release:	2
Group:		Development/Python
URL:		http://www.riverbankcomputing.co.uk/software/sip/intro
Source0:	http://www.riverbankcomputing.com/static/Downloads/sip4/sip-%{version}.tar.gz
License:	GPLv2+
BuildRequires:	bzip2-devel
BuildRequires:	python3-devel
Conflicts:	python-sip
Provides:	python3-sip-api(%{sip_api_major}) = %{sip_api}

%description
SIP is a tool that makes it very easy to create Python bindings for C and C++
libraries. It was originally developed to create PyQt, the Python bindings for
the Qt toolkit, but can be used to create bindings for any C or C++ library.

%files 
%{py3_platsitedir}/s*

%package -n python3-sip-devel
Summary: Files needed to generate Python 3 bindings for any C++ class library
Group: Development/Python
Requires: python3-sip = %{EVRD}
Requires: python3-devel

%description -n python3-sip-devel
This package contains files needed to generate Python 3 bindings for any C++
classes library.

%files -n python3-sip-devel
%{_bindir}/sip
%{py3_incdir}/*
%{_sysconfdir}/rpm/macros.d/sip.macros


#------------------------------------------------------------

%prep
%setup -q -n sip-%{version}

export real_api_major=`grep SIP_API_MAJOR_NR siplib/sip.h.in|head -n1|awk -F' ' '{print $3}'`
export real_api_minor=`grep SIP_API_MINOR_NR siplib/sip.h.in|head -n1|awk -F' ' '{print $3}'`
if [ $real_api_major -ne %{sip_api_major} ]; then
    echo 'Wrong spi major specified: Should be' $real_api_major ', but set' %{sip_api_major}
    exit 1
fi
if [ $real_api_minor -ne %{sip_api_minor} ]; then
    echo 'Wrong spi minor specified: Should be' $real_api_minor ', but set' %{sip_api_minor}
    exit 1
fi

%build

#  Don't use X11R6 prefix for includes neither libraries by default.
for file in specs/linux-*; do
    perl -p -i -e "s@/X11R6/@/@g" $file
done

%{__python3} configure.py
%define _disable_ld_no_undefined 1
%make CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} -fPIC" LIBS="%{?ldflags} -lpython%{py3ver}"

%install
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d/
cat > %{buildroot}%{_sysconfdir}/rpm/macros.d/sip.macros << EOF
# extracted from sip.h, SIP_API_MAJOR_NR SIP_API_MINOR_NR defines
%%sip_api_major %{sip_api_major}
%%sip_api_minor %{sip_api_minor}
%%sip_api       %{sip_api_major}.%{sip_api_minor}
EOF
