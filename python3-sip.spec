Name: python3-sip
Summary: Riverbanks's python sip
Version: 4.12.3
Release: %mkrel 1
Group: Development/Python 
URL: http://www.riverbankcomputing.co.uk/software/sip/intro
Source0: http://www.riverbankcomputing.com/static/Downloads/sip4/sip-%version.tar.gz
License: GPLv2+
BuildRoot: %_tmppath/%name-%version-%release-root
BuildRequires: bzip2-devel
BuildRequires: python3-devel
Conflicts: python-sip

%description
SIP is a tool that makes it very easy to create Python bindings for C and C++ libraries. It was
originally developed to create PyQt, the Python bindings for the Qt toolkit, but can be used to
create bindings for any C or C++ library.

%files 
%defattr(-,root,root)
%_bindir/sip
%py3_platsitedir/s*
%py3_incdir/sip.h

#------------------------------------------------------------

%prep
%setup -q -n sip-%version

%build

#  Don't use X11R6 prefix for includes neither libraries by default.
for file in specs/linux-*; do
    perl -p -i -e "s@/X11R6/@/@g" $file
done

%{__python3} configure.py
%define _disable_ld_no_undefined 1
%{make} CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} -fPIC" LIBS="%{?ldflags} -lpython%{py3ver}"

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

%clean
%{__rm} -rf %{buildroot}
