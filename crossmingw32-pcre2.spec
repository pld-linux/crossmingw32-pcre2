%define		realname	pcre2
Summary:	Perl-Compatible Regular Expression library - MinGW32 cross version
Summary(pl.UTF-8):	Biblioteka perlowych wyrażeń regularnych - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	10.45
Release:	3
License:	BSD (see LICENCE)
Group:		Development/Libraries
Source0:	https://github.com/PhilipHazel/pcre2/releases/download/pcre2-%{version}/%{realname}-%{version}.tar.bz2
# Source0-md5:	f71abbe1b5adf25cd9af5d26ef223b66
URL:		http://www.pcre.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool >= 2:2
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32

%define		_prefix		/usr/%{target}
%define		_libdir		%{_prefix}/lib
%define		_pkgconfigdir	%{_prefix}/lib/pkgconfig
%define		_dlldir		/usr/share/wine/windows/system
%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*
%define		filterout_cxx	-f[-a-z0-9=]*

%description
PCRE stands for the Perl Compatible Regular Expression library. It
contains routines to match text against regular expressions similar to
Perl's. It also contains a POSIX compatibility library.

%description -l pl.UTF-8
PCRE (Perl-Compatible Regular Expression) oznacza bibliotekę wyrażeń
regularnych kompatybilnych z perlowymi. Zawiera funkcje dopasowujące
tekst do wyrażeń regularnych podobnych do tych znanych z Perla.
Zawiera także bibliotekę kompatybilną z POSIX.

%package static
Summary:	Static PCRE libraries (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczne biblioteki PCRE (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static PCRE libraries (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczne biblioteki PCRE (wersja skrośna MinGW32).

%package dll
Summary:	%{realname} - DLL libraries for Windows
Summary(pl.UTF-8):	%{realname} - biblioteki DLL dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
%{realname} - DLL libraries for Windows.

%description dll -l pl.UTF-8
%{realname} - biblioteki DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--host=%{target} \
	--target=%{target} \
	--disable-silent-rules \
	--enable-jit \
	--enable-pcre2-8 \
	--enable-pcre2-16 \
	--enable-pcre2-32

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} $RPM_BUILD_ROOT%{_bindir}/pcre2-config
%{__rm} $RPM_BUILD_ROOT%{_bindir}/*.exe
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{doc,man}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.md ChangeLog LICENCE.md NEWS README
%{_libdir}/libpcre2-8.dll.a
%{_libdir}/libpcre2-16.dll.a
%{_libdir}/libpcre2-32.dll.a
%{_libdir}/libpcre2-posix.dll.a
%{_libdir}/libpcre2-8.la
%{_libdir}/libpcre2-16.la
%{_libdir}/libpcre2-32.la
%{_libdir}/libpcre2-posix.la
%{_includedir}/pcre2*.h
%{_pkgconfigdir}/libpcre2-8.pc
%{_pkgconfigdir}/libpcre2-16.pc
%{_pkgconfigdir}/libpcre2-32.pc
%{_pkgconfigdir}/libpcre2-posix.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpcre2-8.a
%{_libdir}/libpcre2-16.a
%{_libdir}/libpcre2-32.a
%{_libdir}/libpcre2-posix.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpcre2-8-0.dll
%{_dlldir}/libpcre2-16-0.dll
%{_dlldir}/libpcre2-32-0.dll
%{_dlldir}/libpcre2-posix-3.dll
