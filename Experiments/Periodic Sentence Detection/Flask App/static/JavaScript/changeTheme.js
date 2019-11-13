theme = "white"
function changeTheme(){
	if(theme == "white"){
		document.documentElement.style.setProperty('--main-color', '#333333');
		document.documentElement.style.setProperty('--text-color', 'white');
		document.documentElement.style.setProperty('--transparent', '#0000004f');
		document.documentElement.style.setProperty('--next-theme', 'white');
		document.documentElement.style.setProperty('--inactive', 'grey');
		theme="black"
	}
	else{
		document.documentElement.style.setProperty('--main-color', 'white');
		document.documentElement.style.setProperty('--text-color', 'black');
		document.documentElement.style.setProperty('--transparent', '#00000014');
		document.documentElement.style.setProperty('--next-theme', '#333333');
		document.documentElement.style.setProperty('--inactive', '#CCCCCC');
		theme="white"
	}
}