node {
	try {
		stage 'Checkout'
			checkout scm
		stage 'Integration tests '
			sh "echo ${env.BUILD_URL}"

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


