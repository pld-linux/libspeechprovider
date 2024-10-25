# TODO: install and package apidocs
#
# Conditional build:
%bcond_with	apidocs		# API documentation (not installed)
%bcond_without	tests		# unit tests
#
Summary:	Shared library for speech synthesis clients
Summary(pl.UTF-8):	Biblioteka współdzielona dla klientów syntezy mowy
Name:		libspeechprovider
Version:	1.0.3
%define	gitref	SPEECHPROVIDER_%(echo %{version} | tr . _)
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/project-spiel/libspeechprovider/tags
Source0:	https://github.com/project-spiel/libspeechprovider/archive/%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	2bbc4a265d3d7f4bdea8980e9e477f85
URL:		https://project-spiel.org/libspeechprovider/
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 1:2.76
BuildRequires:	meson >= 0.64.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
Requires:	glib2 >= 1:2.76
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The speech provider library is designed to provide some utility for
creating speech providers. Specifically it offers a stream writer that
can be used to send audio data interleaved with speech progress events
(word, sentence, ssml mark, etc.).

%description -l pl.UTF-8
Biblioteka speech-provider jest zaprojektowana, aby zapewnić pewne
narzędzia do tworzenia dostawców mowy. W szczególności oferuje zapis
do strumienia, który może być użyty do wysyłania danych dźwięku w
przeplocie ze zdarzeniami postępu mowy (słowem, zdaniem, znacznikiem
ssml itp.).

%package devel
Summary:	Header files for speech-provider library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki speech-provider
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.76

%description devel
Header files for speech-provider library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki speech-provider.

%package apidocs
Summary:	API documentation for speech-provider library
Summary(pl.UTF-8):	Dokumentacja API biblioteki speech-provider
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for speech-provider library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki speech-provider.

%prep
%setup -q -n %{name}-%{gitref}

%build
%meson build \
	%{!?with_tests:-Dtests=disabled}

%ninja_build -C build

%if %{with tests}
%ninja_test -C build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_libdir}/libspeech-provider-1.0.so
%{_libdir}/girepository-1.0/SpeechProvider-1.0.typelib
%dir %{_datadir}/speech-provider
%{_datadir}/speech-provider/org.freedesktop.Speech.Provider.xml

%files devel
%defattr(644,root,root,755)
%{_includedir}/speech-provider
%{_datadir}/gir-1.0/SpeechProvider-1.0.gir
%{_pkgconfigdir}/speech-provider-1.0.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/speech-provider-1.0
%endif
