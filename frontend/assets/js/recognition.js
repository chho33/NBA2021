$(document).ready(function() {
	
	var bucketRegion = "us-west-2";
	var IdentityPoolId = "us-west-2:9db63bf0-3eb8-48ae-9bfb-9d33623a5f4b";
	
	AWS.config.update({
		region: bucketRegion,
		credentials: new AWS.CognitoIdentityCredentials({
		IdentityPoolId: IdentityPoolId,
		})
	});

	
	
	document.getElementById("input1").onchange = function () {
		var reader = new FileReader();

		reader.onload = function (e) {
			// get loaded data and render thumbnail.
			document.getElementById("image").src = e.target.result;
		};

		// read the image file as a data URL.
		reader.readAsDataURL(this.files[0]);
	}	;
	
	function doSearch(choice, filePath) {
		var bucketName;
		var url;
		if (choice == 1) {
			bucketName = "nba.website";
			url = "https://o2yyl0peqh.execute-api.us-west-2.amazonaws.com/v1/upload"
		}
		else {
			bucketName = "nba.temp";
			url = "https://49hpek9o97.execute-api.us-west-2.amazonaws.com/v1/upload";
		}
		var data = {
						"bucket": bucketName,
						"photoname": filePath
					}
		fetch(url, {
		  method: "POST",
		  body: JSON.stringify(data),
		  headers: {"Content-type": "application/json; charset=UTF-8"}
		})
		.then(response => response.json())
		.then((res) => {
			function replaceAll(string, search, replace) {
			  return string.split(search).join(replace);
			}
			const infoElement = document.getElementById('info');
			console.log(res.body);
			if (choice == 1) {
				var str = replaceAll(res.body, "\\n", "<br>");
				console.log(str);
				infoElement.innerHTML = `<p>${str.slice(1, -1)}</p>`;
			}
			else {
				var results = JSON.parse(res.body);
				var tmp = '<p>';
				for (let index in results) {
					var line1 = results[index].date;
					var line2 = results[index].time;
					var line3 = results[index].home;
					var line4 = results[index].visitor;
					tmp += `${parseInt(index)+1}. ${line1} ${line2} <br> ${line3} vs ${line4} <br><br>`					
				}
				infoElement.innerHTML = tmp += '<\p>'
			}
			
		});	
  }
	
	function s3upload(choice) {  
		var files = document.getElementById('input1').files;
		if (files) 
		{
			var file = files[0];
			var fileName = file.name;
			var filePath = fileName;
			var bucketName;
			if (choice == 1) {
				bucketName = "nba.website/"
			}
			else {
				bucketName = "nba.temp/"
			}
			var fileUrl = 'https://s3-us-west-2.amazonaws.com/' + bucketName +  filePath;
			var s3 = new AWS.S3({
				apiVersion: '2006-03-01',
				params: {Bucket: bucketName}
			});
			s3.upload({
				Key: filePath,
				Body: file,
				ACL: 'public-read'
			}, function(err, data) {
				if(err) {
					console.log(err);
					reject('error');
				}
				
				// alert('Successfully Uploaded!');
			}).on('httpUploadProgress', function (progress) {
				var uploaded = parseInt((progress.loaded * 100) / progress.total);
				$("progress").attr('value', uploaded);
			});
		}
		doSearch(choice, filePath);
	};
	
	$('#button1').click(function() {
		s3upload(1);
  });
	
	$('#button2').click(function() {
		s3upload(2);
  });

});