gen elite = 0
replace elite = 1 if futprice >= 20000

gen is10 = 0
replace is10 = 1 if jerseynumber == 10

gen eliteClub = 0

replace eliteClub = 1 if (club == "Real Madrid") | (club == "Paris Saint-Germain") | (club == "Juventus") | (club == "FC Barcelona") | (club == "Atletico Madrid") | (club == "Chelsea") | (club == "Manchester City") | (club == "Tottenham Hotspur") | club == ("Manchester United") | (club == "Liverpool") 

unab xvars: finishing dribbling sprintspeed gkreflexes

gen wMaxSkills = "" 
gen maxSkills = 0 

quietly foreach x of local xvars { 
   replace wMaxSkills = "`x'" if `x' > maxSkills
   replace maxSkills = `x' if `x' > maxSkills
}

unab xvars2: ls st rs lw lf cf rf rw lam cam ram lm lcm cm rcm rm lwb ldm cdm rdm rwb lb lcb cb rcb rb 

gen wMaxPos = "" 
gen maxPos = 0 

quietly foreach x of local xvars2 { 
    replace wMaxPos = "`x'" if `x' > maxPos     
    replace maxPos = `x' if `x' > maxPos
}

gen lnfutprice = ln(futprice)

gen forward = 0
replace forward = 1 if (position == "ST") | (position == "RF") | (position == "LF") | (position == "LS") | (position == "RS")

gen faceCard = 0
replace faceCard = 1 if realface == "Yes"

gsort -lnfutprice

reg lnfutprice potential maxSkills eliteClub is10 forward overall maxPos if elite == 1, robust
