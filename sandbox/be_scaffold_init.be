{
	config: {
		build_mode: [dev, test, prod]
	},
	app_name: "undefined",
	models: [
		{ model1:	"fieldA(number[max_length=3])",
					"fieldB(string[])", "fieldC()", "fieldD",... },
		{ model2: 	"fieldA(number[max_length=3])", 
					"fieldB(string)", "fieldC()", "fieldD",... },
		{ model3: 	"fieldA(number[max_length=3])", 
					"fieldB(string)", "fieldC()", "fieldD",... },
		{ model4: 	"fieldA(number[max_length=3,auto_gen=True])", 
					"fieldB(string)", "fieldC()", "fieldD",... }
	],
	routes: [
		"model1-[LIST]->{}",
		"model2-[LIST]->{}",
		"model3-[LIST]->{}",
		"model2(fieldA -> model3(fieldA, fieldB))-[LIST]->{}",
		"model4(fieldA -> model3(fieldA, fieldB))<-[POST]-{}"
	]
}
