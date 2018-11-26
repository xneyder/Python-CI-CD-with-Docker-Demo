node {
	try {
		stage 'Checkout'
			checkout scm
		stage 'Integration tests '
			sh "docker-compose -f docker-compose-qa.yml up --force-recreate --abort-on-container-exit --build"
			sh 'pwd'
	}
	catch(err) {
			mail body: "project build error is here: ${env.BUILD_URL}" ,
       		     	from: 'xneyder@gmail.com',
			replyTo: 'xneyder@gmail.com',
       		     	subject: 'project build failed',
			to: 'xneyder@gmail.com'
		throw err
	}
}


