node {
	try {
		stage 'Checkout'
			checkout scm
		stage 'Integration tests '
			sh 'pwd'
			sh "docker-compose -f docker-compose-qa.yml up --force-recreate --abort-on-container-exit --build"
			sh "ls ./app/tests/integration/test-reports/*xml"

	}
	catch(err) {
			mail body: "project test error is here: ${env.BUILD_URL}" ,
       		     	from: 'xneyder@gmail.com',
			replyTo: 'xneyder@gmail.com',
       		     	subject: 'project test failed',
			to: 'xneyder@gmail.com'
		throw err
	} 
	finally {
		junit 'app/tests/integration/test-reports/*xml'
	}
}


