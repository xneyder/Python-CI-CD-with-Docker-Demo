node {
	stage 'Checkout'
		checkout scm
	stage 'Integration tests '
		sh "docker-compose -f docker-compose-qa.yml up --force-recreate --abort-on-container-exit --build"
		sh 'ls'
}

