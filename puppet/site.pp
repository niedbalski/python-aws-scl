Exec { path => "/bin:/sbin:/usr/bin:/usr/sbin" }

class git::clone ($github_user='niedbalski', $repo, $username='ubuntu') {

    $group = $username

    group { $username:
        ensure  => present
    }

    user { $username:
        ensure  => present,
        gid     => $group,
        require => Group[$group],
        uid     => 2000,
        home    => "/home/${username}",
        shell   => "/bin/bash",
        managehome  => true,
    }

    file { '/home/ubuntu/code/' :
        ensure  => directory,
        group   => $group,
        owner   => $username,
        mode    => 0755,
    }

    file { '/home/${username}':
        ensure  => directory,
        group   => $group,
        owner   => $username,
        mode    => 0700,
    }

    package { 'git':
        ensure => installed,
    }
    
    vcsrepo { "/home/ubuntu/code/${repo}":
        ensure   => latest,
        owner    => $owner,
        group    => $owner,
        provider => git,
        require  => [ Package["git"] ],
        source   => "http://github.com/${github_user}/${repo}.git",
        revision => 'master',
    }
}

class git {
        class { git::clone: 
		github_user => 'niedbalski',
		repo => 'flask-hello-world',
	}
}

class { 'python':
   gunicorn => true,
   pip => true,
}

class reqs {
   file { '/home/ubuntu/code/flask-hello-world/requirements.txt':
	ensure => present
   }

   python::requirements { '/home/ubuntu/code/flask-hello-world/requirements.txt':
	owner => 'root'
   }
 
   pip::install { "flask": }

   python::gunicorn { 'localhost':
  	ensure      => present,
  	mode        => 'wsgi',
  	dir         => '/home/ubuntu/code/flask-hello-world',
  	bind        => 'localhost:10000',
   }
}

node default {
   class { git: }
   class { reqs: }
}
