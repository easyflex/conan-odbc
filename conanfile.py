import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class OdbcConan(ConanFile):
    name = 'odbc'
    version = '2.3.5'
    description = 'Package providing unixODBC or Microsoft ODBC'
    url = 'https://github.com/bincrafters/conan-odbc'

    license = 'LGPL/GPL'
    exports = ['LICENSE.md']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'fPIC': [True, False]}
    default_options = 'shared=False', 'fPIC=True'

    def configure(self):
        del self.settings.compiler.libcxx  # Pure C
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def source(self):
        if self.settings.os == 'Windows':
            return
        v = self.version
        source_url = 'https://iweb.dl.sourceforge.net/project/unixodbc/unixODBC/%s/unixODBC-%s.tar.gz' % (v, v)
        tools.get(source_url)
        self.source_dir = 'unixODBC-%s' % self.version

    def build(self):
        if self.settings.os == 'Windows':
            return
        env_build = AutoToolsBuildEnvironment(self)
        static_flag = 'no' if self.options.shared else 'yes'
        shared_flag = 'yes' if self.options.shared else 'no'
        args = ['--enable-static=%s' % static_flag, '--enable-shared=%s' % shared_flag, '--enable-ltdl-install']
        if self.options.fPIC:
            args.append('--with-pic=yes')
        with tools.chdir(self.source_dir):
            env_build.configure(args=args)
            env_build.make(args=['-j16'])

    def package(self):
        if self.settings.os == 'Windows':
            return

        files = {
            '': ['LICENSE*'],
            'include': [
                'include/autotest.h',
                'libltdl/ltdl.h',
                'include/odbcinst.h',
                'include/odbcinstext.h',
                'include/sql.h',
                'include/sqlext.h',
                'include/sqlspi.h',
                'include/sqltypes.h',
                'include/sqlucode.h',
                'unixodbc_conf.h',
                'include/uodbc_extras.h',
                'include/uodbc_stats.h',
            ],
            'lib': [
                'libltdl/.libs/libltdl.*',
                'DriverManager/.libs/libodbc.*',
                'cur/.libs/libodbccr.*',
                'odbcinst/.libs/libodbcinst.*',
            ],
            'bin': [
                'exe/dltest',
                'exe/isql',
                'exe/iusql',
                'exe/odbc_config',
                'exe/odbcinst',
                'exe/slencheck',
            ]
        }

        for dst, patterns in files.items():
            for pattern in patterns:
                self.copy(pattern, src=self.source_dir, dst=dst, keep_path=False)

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))

        if self.settings.os == 'Windows':
            self.cpp_info.libs = ['odbc32', 'odbccp32']
        else:
            self.cpp_info.libs = ['odbc', 'odbccr', 'odbcinst', 'ltdl']
            if self.settings.os == 'Linux':
                self.cpp_info.libs.append('dl')
            elif self.settings.os == 'Macos':
                self.cpp_info.libs.append('iconv')
