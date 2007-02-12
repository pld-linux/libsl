#
# NOTE:	renamed to avoid conflict with sl.spec/pkg
#
# Conditional build:
%bcond_without	static_libs # don't build static libraries
#
Summary:	A small and flexible linked list implementation
Summary(pl.UTF-8):   Mała i elastyczna implementacja listy wiązanej
Name:		libsl
Version:	0.3.4
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://dev.brautaset.org/sl/download/sl-%{version}.tar.gz
# Source0-md5:	56d9ac18ca92436ff05ffee8ef23cdb9
Patch0:		%{name}-am.patch
URL:		http://brautaset.org/software/sl/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	libtool
# pod2man
BuildRequires:	perl-tools-pod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sl is a memory-efficient generic linked list library. It doesn't use
container nodes. Instead it requires a pointer to the next item
directly in the datastructure you want to create lists (or stacks) of.
This can give you significant memory savings when creating long lists
of small structures. It also allows for fast push and pop operations
since there is no need to allocate or free memory for the container
nodes. It also means that a push can't fail because memory couldn't be
allocated for the container node.

%description -l pl.UTF-8
sl to wydajna pamięciowo biblioteka ogólnych list wiązanych. Nie używa
węzłów kontenerowych. Zamiast tego wymaga wskaźnika do następnego
elementu bezpośrednio w strukturze danych, z której chce się utworzyć
listy (lub stosy). Może to dać znaczącą oszczędność pamięci przy
tworzeniu długich list małych struktur. Pozwala także na szybkie
operacje "push" i "pop", jako że nie ma potrzeby przydzielania i
zwalniania pamięci dla węzłów kontenerowych. Oznacza to także, że
operacja "push" nie może nie powieść się z powodu niemożności
przydzielenia pamięci na węzeł kontenerowy.

%package devel
Summary:	Header files for libsl library
Summary(pl.UTF-8):   Pliki nagłówkowe biblioteki libsl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libsl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsl.

%package static
Summary:	Static libsl library
Summary(pl.UTF-8):   Statyczna biblioteka libsl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libsl library.

%description static -l pl.UTF-8
Statyczna biblioteka libsl.

%prep
%setup -q -n sl-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_static_libs:--enable-static=no}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libsl.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsl.so
%{_libdir}/libsl.la
%{_includedir}/sl
%{_mandir}/man3/sl.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsl.a
%endif
