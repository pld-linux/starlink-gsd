Summary:	GSD - the Global Section Datafile (GSD) access library
Summary(pl):	GSD - biblioteka dostêpu do plików GDS (Global Section Datafile)
Name:		starlink-gsd
Version:	1.0.218
Release:	2
License:	non-commercial use and distribution (see GSD_CONDITIONS)
Group:		Libraries
Source0:	ftp://ftp.starlink.rl.ac.uk/pub/ussc/store/gsd/gsd.tar.Z
# Source0-md5:	7eba2784a35a981c12e9108f836a5cd2
Patch0:		%{name}-endian.patch
URL:		http://www.starlink.rl.ac.uk/static_www/soft_further_GSD.html
BuildRequires:	gcc-g77
BuildRequires:	sed >= 4.0
BuildRequires:	starlink-cnf-devel
BuildRequires:	starlink-sae-devel
Requires:	starlink-sae
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		stardir		/usr/lib/star

%description
This package contains Global Section Datafile (GSD) access library.
This library provides read-only access to GSD files created at the
James Clerk Maxwell Telescope.

%description -l pl
Ten pakiet zawiera bibliotekê dostêpu do plików GSD (Global Section
Datafile - plików danych sekcji globalnej). Biblioteka umo¿liwia
dostêp tylko do odczytu do plików GSD tworzonych przez teleskop
James Clerk Maxwell Telescope.

%package devel
Summary:	Header files for GSD library
Summary(pl):	Pliki nag³ówkowe biblioteki GSD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	starlink-cnf-devel

%description devel
Header files for GSD library.

%description devel -l pl
Pliki nag³ówkowe biblioteki GSD.

%package static
Summary:	Static Starlink GSD library
Summary(pl):	Statyczna biblioteka Starlink GSD
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Starlink GSD library.

%description static -l pl
Statyczna biblioteka Starlink GSD.

%prep
%setup -q -c

mkdir tmp
cd tmp
tar xf ../gsd_source.tar
%patch0 -p1
tar cf ../gsd_source.tar *
cd ..
rm -rf tmp

sed -i -e "s/ -O'/ %{rpmcflags} -fPIC'/;s/ ld -shared -soname / %{__cc} -shared \\\$\\\$3 -Wl,-soname=/" mk
sed -i -e "s/-L\\\$(STAR_LIB)/-L\\\$(STARLINK)\\/share/" makefile

%build
SYSTEM=ix86_Linux \
./mk build \
	STARLINK=%{stardir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{stardir}/help

SYSTEM=ix86_Linux \
./mk install \
	STARLINK=%{stardir} \
	INSTALL=$RPM_BUILD_ROOT%{stardir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc GSD_CONDITIONS gsd.news
%{stardir}/dates/*
%docdir %{stardir}/docs
%{stardir}/docs/sun*
%attr(755,root,root) %{stardir}/share/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{stardir}/bin/gsd_dev
%attr(755,root,root) %{stardir}/bin/gsd_link*
%{stardir}/include/*

%files static
%defattr(644,root,root,755)
%{stardir}/lib/*.a
