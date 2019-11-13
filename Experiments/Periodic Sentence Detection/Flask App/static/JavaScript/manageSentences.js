//Variables
sentenceID = 0;
var summarySentences = document.getElementsByClassName("summarySentence");
var sentences = document.getElementsByClassName("sentence");
var sentenceDots = document.getElementsByClassName("sentenceDot");
counters = document.getElementsByClassName('counter');
activeTab = "summary";

window.onload = initialisePage();
window.onload = openTab('summary');

function openTab(tabName) {
  	var tabs = document.getElementsByClassName("tab");
  	var tabButtons = document.getElementsByClassName("tabButton");
	for (var i = 0; i < tabs.length; i++) {
  	  	tabs[i].style.display = "none"; 
		tabButtons[i].style.color = "var(--text-color)";
		tabButtons[i].setAttribute('active', 'false');
  	}
  	document.getElementById(tabName).style.display = "block"; 
	document.getElementById(tabName+'Button').setAttribute('active', 'true');
	activeTab = tabName;
	sentenceID = 0;
	clearSentences();
	sentences[sentenceID].style.display = "block";
	if(summarySentences.length > 0){
		summarySentences[sentenceID].style.display = "flex";
	}
	changeButtons();
}

function nextSentence(){
	if(activeTab == "summary"){
		if(sentenceID < summarySentences.length-1){
			clearSentences();
			sentenceID = sentenceID + 1;
			summarySentences[sentenceID].style.display = "flex";		
			changeButtons();
		}
	}
	else{
		if(sentenceID < sentences.length-1){
			clearSentences();
			sentenceID = sentenceID + 1;
			sentences[sentenceID].style.display = "block";			
			changeButtons();
		}
	}		
}

function prevSentence(){
	if(activeTab == "summary"){
		if(sentenceID > 0){
			clearSentences();
			sentenceID = sentenceID - 1;
			summarySentences[sentenceID].style.display = "flex";	
			changeButtons();
		}	
	} 
	else {
		if(sentenceID > 0){
			clearSentences();
			sentenceID = sentenceID - 1;
			sentences[sentenceID].style.display = "block";		
			changeButtons();
		}	
	}
}

function sentenceSet(index){
	clearSentences();
	sentenceID = index;
	sentences[sentenceID].style.display = "block";	
	changeButtons();	
}

function changeButtons(){
	sentenceNum = 0;
	prevButton = null;
	nextButton = null;

	if(activeTab == "sentences"){
		sentenceNum = sentences.length-1;
		prevButton = document.getElementById("prevSentence");
		nextButton = document.getElementById("nextSentence");
	}
	else if(document.getElementById("prevSumSentence") != null && document.getElementById("nextSumSentence") != null)
	{
		sentenceNum = summarySentences.length-1;
		prevButton = document.getElementById("prevSumSentence");
		nextButton = document.getElementById("nextSumSentence");
	}

	if(prevButton != null && nextButton != null){
		if(sentenceID > 0){
			prevButton.setAttribute('active', 'true');
		}
		else{
			prevButton.setAttribute('active', 'false');
		}

		if(sentenceID < sentenceNum){
			nextButton.setAttribute('active', 'true');
		}
		else{
			nextButton.setAttribute('active', 'false');
		}
	}
	
	if(activeTab == "sentences"){
		for(var counter of counters){
			counter.innerHTML = sentenceID+1 + " of " + sentences.length;
		}
		sentenceDots[sentenceID].style.background = "var(--accent)";
	}
}

function clearSentences(){
	for (var i = 0; i < sentences.length; i++) {
		sentences[i].style.display = "none"; 
		sentenceDots[i].style.background = "var(--inactive)";
	}
	if(summarySentences.length > 0){
		for (var i = 0; i < summarySentences.length; i++) {
			summarySentences[i].style.display = "none"; 
		}
	}	
}

function initialisePage(){
	for (var i = 0; i < sentences.length; i++) {
		sentences[i].style.display = "none"; 
		sentenceDots[i].style.background = "var(--inactive)";
	}
	sentences[sentenceID].style.display = "block";
	changeButtons();
}