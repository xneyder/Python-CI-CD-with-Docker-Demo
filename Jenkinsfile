node {
	try {
		stage 'Checkout'
			checkout scm
		stage 'Integration tests '
			sh "docker-compose -f docker-compose-qa.yml up --force-recreate --abort-on-container-exit --build"
		stage 'Deploy'
			sh "echo 'Deployed Locally'"

	}
	catch(err) {
			mail body: "project test error is here: ${env.BUILD_URL}" ,
       		     	from: 'xneyder@gmail.com',
			replyTo: 'xneyder@gmail.com',
       		     	subject: 'project test failed',
			to: 'danielj@teoco.com'
		throw err
	} 
	finally {
		junit 'app/tests/integration/test-reports/*xml'
	}
}


