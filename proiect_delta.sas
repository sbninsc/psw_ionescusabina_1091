/*import date*/
proc import datafile="/home/u64501193/proiect/esantion_delta.csv"
	out=delta_raw
	dbms=csv
	replace;
	getnames=yes;
run;

proc contents data=delta_raw; run;
proc print data=delta_raw (obs=10); run;

/*formate definite utilizator*/
proc format;
    value $delay
        'Weather'   = 'Intarziere meteo'
        'Technical' = 'Probleme tehnice'
        'Crew'      = 'Echipaj'
        'Other'     = 'Altele'
        OTHER       = 'Necunoscut';

    value cancelfmt
        0 = 'Nu'
        1 = 'Da';

    value divertfmt
        0 = 'Nu'
        1 = 'Da';
run;

data delta_fmt;
	set delta_raw;
	format DelayReason $delay.
		   Cancelled cancelfmt.
		   Diverted divertfmt.;
run;

/*procesare iterativa/conditionala*/
data delta_proc;
	set delta_fmt;
	if DelayMinutes>0 or Cancelled=1 or Diverted=1 then ProblemFlight = 1;
	else ProblemFlight=0;
	TotalCount=0;
	do i=1 to DelayMinutes;
		TotalCount+1;
	end;
	drop i;
run;

/*fct sas*/
data delta_func;
	set delta_proc;
	ScheduledDuration=intck('minute', ScheduledDeparture, ScheduledArrival);
	ActualDuration=intck('minute', ActualDeparture, ActualArrival);
	DurationDiff=ActualDuration-ScheduledDuration;
	FlightMonth = month(datepart(ScheduledDeparture));
run;



/*statistici*/
proc univariate data=delta_fmt plot;
var DelayMinutes;
title "Distributia intarzierilor";
run;

proc means data=delta_func n mean std min max;
class Destination;
var DelayMinutes ActualDuration;
title "Statistici pe destinatii";
run;







