#
# NOTE:	renamed to avoid conflict with sl.spec/pkg
#
# Conditional build:
%bcond_without	static_libs # don't build static libraries
#
Summary:	A small and flexible linked list implementation
Summary(pl):	Ma�a i elastyczna implementacja listy wi�zanej.
Name:		libsl
Version:	0.3.2
Release:	0.1
License:	GPL v2
Group:		Libraries
Source0:	http://brautaset.org/software/sl/download/sl-%{version}.tar.gz
# Source0-md5:	d1b2d7b4e1ed266e901bf1c177bbba8d
URL:		http://brautaset.org/software/sl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
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

#%%description -l pl

%package devel
Summary:	Header files for libsl library
Summary(pl):	Pliki nag��wkowe biblioteki libsl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libsl library.

%description devel -l pl
Pliki nag��wkowe biblioteki libsl.

%package static
Summary:	Static libsl library
Summary(pl):	Statyczna biblioteka libsl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libsl library.

%description static -l pl
Statyczna biblioteka libsl.

%prep
%setup -q -n sl-%{version}

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
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/sl
%{_mandir}/man3/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif