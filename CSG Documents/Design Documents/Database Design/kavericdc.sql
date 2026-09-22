--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6
-- Dumped by pg_dump version 15.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: kavericdc; Type: SCHEMA; Schema: -; Owner: csgadmin
--

CREATE SCHEMA kavericdc;


ALTER SCHEMA kavericdc OWNER TO csgadmin;

--
-- Name: fn_ams_reg_epaymentamtpaid_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
        insert into kavericdc.ams_reg_epaymentamtpaiddetails_audit 
		(username,"action",query,chlnrefnum,deptpurposeid,headofaccount,amountpaid,applicationnumber,deptreferencecode,totalamount,id,inserteddatetime,k1k2_flag
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
	old.chlnrefnum,old.deptpurposeid,old.headofaccount,old.amountpaid,old.applicationnumber,old.deptreferencecode,old.totalamount,old.id,old.inserteddatetime,old.k1k2_flag
	); return new;	
		
	elsif tg_op = 'DELETE' then
       insert into kavericdc.ams_reg_epaymentamtpaiddetails_audit 
		(
    username ,	action ,	query ,
	chlnrefnum,deptpurposeid,headofaccount,amountpaid,applicationnumber,deptreferencecode,totalamount,id,inserteddatetime,k1k2_flag
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
	old.chlnrefnum,old.deptpurposeid,old.headofaccount,old.amountpaid,old.applicationnumber,old.deptreferencecode,old.totalamount,old.id,old.inserteddatetime,old.k1k2_flag
	); return old;
    
	elsif tg_op = 'INSERT' then
	
	insert into kavericdc.ams_reg_epaymentamtpaiddetails_audit 
		(
    username ,	action ,	query ,
	chlnrefnum,deptpurposeid,headofaccount,amountpaid,applicationnumber,deptreferencecode,totalamount,id,inserteddatetime,k1k2_flag
	)
    values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
	NEW.chlnrefnum,NEW.deptpurposeid,NEW.headofaccount,NEW.amountpaid,NEW.applicationnumber,NEW.deptreferencecode,NEW.totalamount,NEW.id,NEW.inserteddatetime,NEW.k1k2_flag
	); return new;
	
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() OWNER TO csgadmin;

--
-- Name: fn_ams_reg_epaymentbankackdetails_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
        insert into kavericdc.ams_reg_epaymentbankackdetails_audit 
		(username,"action",query,deptreferencecode,banktransactionnumber,bankname,paymentmode,paymentstatuscode,transactiontimestamp,amount,checksum,transactionid,bankackid,inserteddatetime,k1k2_flag
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
	Old.deptreferencecode,Old.banktransactionnumber,Old.bankname,Old.paymentmode,Old.paymentstatuscode,Old.transactiontimestamp,Old.amount,Old.checksum,Old.transactionid,Old.bankackid,Old.inserteddatetime,Old.k1k2_flag
	); return new;	
		
	elsif tg_op = 'DELETE' then
       insert into kavericdc.ams_reg_epaymentbankackdetails_audit 
		(
    username ,	action ,	query ,deptreferencecode,banktransactionnumber,bankname,paymentmode,paymentstatuscode,transactiontimestamp,amount,checksum,transactionid,bankackid,inserteddatetime,k1k2_flag
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
	Old.deptreferencecode,Old.banktransactionnumber,Old.bankname,Old.paymentmode,Old.paymentstatuscode,Old.transactiontimestamp,Old.amount,Old.checksum,Old.transactionid,Old.bankackid,Old.inserteddatetime,Old.k1k2_flag
	); return old;
    
	elsif tg_op = 'INSERT' then
	
	insert into kavericdc.ams_reg_epaymentbankackdetails_audit 
		(
    username ,	action ,	query ,deptreferencecode,banktransactionnumber,bankname,paymentmode,paymentstatuscode,transactiontimestamp,amount,checksum,transactionid,bankackid,inserteddatetime,k1k2_flag
	)
    values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
	New.deptreferencecode,New.banktransactionnumber,New.bankname,New.paymentmode,New.paymentstatuscode,New.transactiontimestamp,New.amount,New.checksum,New.transactionid,New.bankackid,New.inserteddatetime,New.k1k2_flag
	); return new;
	
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() OWNER TO csgadmin;

--
-- Name: fn_ams_reg_epaymenttransdetails_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
        insert into kavericdc.ams_reg_epaymenttransdetails_audit 
		(username,"action",query,applicationid,officeid,remittername,totalamount,receiptid,chlnrefnum,deptreferencecode,uirnumber,statuscode,statusdescription,transactionstatus,transactiondatetime,userid,ipadd,serviceid,paymentstatuscode,ecid,ccid,epid,applicationnumber,treasurycode,transactionid,ddocode,isdelete,lastupdateddate,documentid,feerulecode,inserteddatetime,k1k2_flag
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
	old.applicationid,old.officeid,old.remittername,old.totalamount,old.receiptid,old.chlnrefnum,old.deptreferencecode,old.uirnumber,old.statuscode,old.statusdescription,old.transactionstatus,old.transactiondatetime,old.userid,old.ipadd,old.serviceid,old.paymentstatuscode,old.ecid,old.ccid,old.epid,old.applicationnumber,old.treasurycode,old.transactionid,old.ddocode,old.isdelete,old.lastupdateddate,old.documentid,old.feerulecode,old.inserteddatetime,old.k1k2_flag
	); return new;	
		
	elsif tg_op = 'DELETE' then
       insert into kavericdc.ams_reg_epaymenttransdetails_audit 
		(
    username ,	action ,	query ,
	applicationid,officeid,remittername,totalamount,receiptid,chlnrefnum,deptreferencecode,uirnumber,statuscode,statusdescription,transactionstatus,transactiondatetime,userid,ipadd,serviceid,paymentstatuscode,ecid,ccid,epid,applicationnumber,treasurycode,transactionid,ddocode,isdelete,lastupdateddate,documentid,feerulecode,inserteddatetime,k1k2_flag
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
	old.applicationid,old.officeid,old.remittername,old.totalamount,old.receiptid,old.chlnrefnum,old.deptreferencecode,old.uirnumber,old.statuscode,old.statusdescription,old.transactionstatus,old.transactiondatetime,old.userid,old.ipadd,old.serviceid,old.paymentstatuscode,old.ecid,old.ccid,old.epid,old.applicationnumber,old.treasurycode,old.transactionid,old.ddocode,old.isdelete,old.lastupdateddate,old.documentid,old.feerulecode,old.inserteddatetime,old.k1k2_flag
	); return old;
    
	elsif tg_op = 'INSERT' then
	
	insert into kavericdc.ams_reg_epaymenttransdetails_audit 
		(
    username ,	action ,	query ,
	applicationid,officeid,remittername,totalamount,receiptid,chlnrefnum,deptreferencecode,uirnumber,statuscode,statusdescription,transactionstatus,transactiondatetime,userid,ipadd,serviceid,paymentstatuscode,ecid,ccid,epid,applicationnumber,treasurycode,transactionid,ddocode,isdelete,lastupdateddate,documentid,feerulecode,inserteddatetime,k1k2_flag
	)
    values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
	New.applicationid,New.officeid,New.remittername,New.totalamount,New.receiptid,New.chlnrefnum,New.deptreferencecode,New.uirnumber,New.statuscode,New.statusdescription,New.transactionstatus,New.transactiondatetime,New.userid,New.ipadd,New.serviceid,New.paymentstatuscode,New.ecid,New.ccid,New.epid,New.applicationnumber,New.treasurycode,New.transactionid,New.ddocode,New.isdelete,New.lastupdateddate,New.documentid,New.feerulecode,New.inserteddatetime,New.k1k2_flag
	); return new;
	
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() OWNER TO csgadmin;

--
-- Name: fn_application_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_application_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
        insert into kavericdc.applicantapplication_audit 
		(
    username ,	action ,	query , 	
	citizenid  ,
	applicationnumber  ,
	srocode  ,
	regsrocode  ,
	applicationtypeid  ,
	applicationstartdate ,
	applicationenddate  ,
	currentstatus  ,
	assignedto  ,
	aroapplicationnumber  ,
	stamparticlecode  ,
	stampruleid  ,
	deedattachpath  ,
	registrationstartdate  ,
	registrationenddate  ,
	lastupdatedby  ,
	regarticlecode  ,
	bookid  ,
	remarks  ,
	sfdaid  ,
	deoid  ,
	applicationdate  ,
	issubmitted    ,
	isduecorrection    ,
	ispayment  ,
	isdueschedule  ,
	annexurepath  ,
	k1k2_flag ,
	inserteddatetime ,
	refuseremarks  ,
	remarksk,
	isdeleted,
	ispaperless,
	ispanverified,ispanmandatory
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
	old.citizenid  ,
	old.applicationnumber  ,
	old.srocode  ,
	old.regsrocode  ,
	old.applicationtypeid  ,
	old.applicationstartdate ,
	old.applicationenddate  ,
	old.currentstatus  ,
	old.assignedto  ,
	old.aroapplicationnumber  ,
	old.stamparticlecode  ,
	old.stampruleid  ,
	old.deedattachpath  ,
	old.registrationstartdate  ,
	old.registrationenddate  ,
	old.lastupdatedby  ,
	old.regarticlecode  ,
	old.bookid  ,
	old.remarks  ,
	old.sfdaid  ,
	old.deoid  ,
	old.applicationdate  ,
	old.issubmitted    ,
	old.isduecorrection    ,
	old.ispayment  ,
	old.isdueschedule  ,
	old.annexurepath  ,
	old.k1k2_flag ,
	old.inserteddatetime ,
	old.refuseremarks  ,
	old.remarksk,
	old.isdeleted,old.ispaperless,
	old.ispanverified,old.ispanmandatory
	); return new;	
		
	elsif tg_op = 'DELETE' then
       insert into kavericdc.applicantapplication_audit 
		(
    username ,	action ,	query ,
	citizenid  ,
	applicationnumber  ,
	srocode  ,
	regsrocode  ,
	applicationtypeid  ,
	applicationstartdate ,
	applicationenddate  ,
	currentstatus  ,
	assignedto  ,
	aroapplicationnumber  ,
	stamparticlecode  ,
	stampruleid  ,
	deedattachpath  ,
	registrationstartdate  ,
	registrationenddate  ,
	lastupdatedby  ,
	regarticlecode  ,
	bookid  ,
	remarks  ,
	sfdaid  ,
	deoid  ,
	applicationdate  ,
	issubmitted    ,
	isduecorrection    ,
	ispayment  ,
	isdueschedule  ,
	annexurepath  ,
	k1k2_flag ,
	inserteddatetime ,
	refuseremarks  ,
	remarksk,
	isdeleted,ispaperless,
	ispanverified,ispanmandatory
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
	old.citizenid  ,
	old.applicationnumber  ,
	old.srocode  ,
	old.regsrocode  ,
	old.applicationtypeid  ,
	old.applicationstartdate ,
	old.applicationenddate  ,
	old.currentstatus  ,
	old.assignedto  ,
	old.aroapplicationnumber  ,
	old.stamparticlecode  ,
	old.stampruleid  ,
	old.deedattachpath  ,
	old.registrationstartdate  ,
	old.registrationenddate  ,
	old.lastupdatedby  ,
	old.regarticlecode  ,
	old.bookid  ,
	old.remarks  ,
	old.sfdaid  ,
	old.deoid  ,
	old.applicationdate  ,
	old.issubmitted    ,
	old.isduecorrection    ,
	old.ispayment  ,
	old.isdueschedule  ,
	old.annexurepath  ,
	old.k1k2_flag ,
	old.inserteddatetime ,
	old.refuseremarks  ,
	old.remarksk,
	old.isdeleted,old.ispaperless,
	old.ispanverified,old.ispanmandatory
	); return old;
    
	elsif tg_op = 'INSERT' then
	
	insert into kavericdc.applicantapplication_audit 
		(
    username ,	action ,	query ,
	citizenid  ,
	applicationnumber  ,
	srocode  ,
	regsrocode  ,
	applicationtypeid  ,
	applicationstartdate ,
	applicationenddate  ,
	currentstatus  ,
	assignedto  ,
	aroapplicationnumber  ,
	stamparticlecode  ,
	stampruleid  ,
	deedattachpath  ,
	registrationstartdate  ,
	registrationenddate  ,
	lastupdatedby  ,
	regarticlecode  ,
	bookid  ,
	remarks  ,
	sfdaid  ,
	deoid  ,
	applicationdate  ,
	issubmitted    ,
	isduecorrection    ,
	ispayment  ,
	isdueschedule  ,
	annexurepath  ,
	k1k2_flag ,
	inserteddatetime ,
	refuseremarks  ,
	remarksk,
	isdeleted,ispaperless,
	ispanverified,ispanmandatory
	)
    values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
	new.citizenid  ,
	new.applicationnumber  ,
	new.srocode  ,
	new.regsrocode  ,
	new.applicationtypeid  ,
	new.applicationstartdate ,
	new.applicationenddate  ,
	new.currentstatus  ,
	new.assignedto  ,
	new.aroapplicationnumber  ,
	new.stamparticlecode  ,
	new.stampruleid  ,
	new.deedattachpath  ,
	new.registrationstartdate  ,
	new.registrationenddate  ,
	new.lastupdatedby  ,
	new.regarticlecode  ,
	new.bookid  ,
	new.remarks  ,
	new.sfdaid  ,
	new.deoid  ,
	new.applicationdate  ,
	new.issubmitted    ,
	new.isduecorrection    ,
	new.ispayment  ,
	new.isdueschedule  ,
	new.annexurepath  ,
	new.k1k2_flag ,
	new.inserteddatetime ,
	new.refuseremarks  ,
	new.remarksk,
	new.isdeleted,new.ispaperless,
	new.ispanverified,new.ispanmandatory
	); return new;
	
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_application_audit() OWNER TO csgadmin;

--
-- Name: fn_appointmentmaster_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_appointmentmaster_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.appointmentmaster_audit
		( username ,	action ,	query , appointmentid,appointmenttypeid,srocode,deoperator,applicationnumber,appointmentdate,starttime,endtime,noofapplicants,status,k1k2_flag,inserteddatetime,reschedulefrmtool
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.appointmentid,old.appointmenttypeid,old.srocode,old.deoperator,old.applicationnumber,old.appointmentdate,old.starttime,old.endtime,old.noofapplicants,old.status,old.k1k2_flag,old.inserteddatetime,old.reschedulefrmtool); return new;	
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.appointmentmaster_audit
		( username ,	action ,	query , appointmentid,appointmenttypeid,srocode,deoperator,applicationnumber,appointmentdate,starttime,endtime,noofapplicants,status,k1k2_flag,inserteddatetime,reschedulefrmtool
		)
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.appointmentid,old.appointmenttypeid,old.srocode,old.deoperator,old.applicationnumber,old.appointmentdate,old.starttime,old.endtime,old.noofapplicants,old.status,old.k1k2_flag,old.inserteddatetime,old.reschedulefrmtool); return old;
    
	elsif tg_op = 'INSERT' then
	insert into kavericdc.appointmentmaster_audit
		( username ,	action ,	query , appointmentid,appointmenttypeid,srocode,deoperator,applicationnumber,appointmentdate,starttime,endtime,noofapplicants,status,k1k2_flag,inserteddatetime,reschedulefrmtool
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		New.appointmentid,New.appointmenttypeid,New.srocode,New.deoperator,New.applicationnumber,New.appointmentdate,New.starttime,New.endtime,New.noofapplicants,New.status,New.k1k2_flag,New.inserteddatetime,New.reschedulefrmtool); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_appointmentmaster_audit() OWNER TO csgadmin;

--
-- Name: fn_cc_applicationdetails_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_cc_applicationdetails_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.cc_applicationdetails_audit
		( username ,	action ,	query , 
		ccid,ccnumber,ccdate,userid,documenttype,kaveridrocode,kaverisrocode,documentnumber,booktype,yearofregistration,pagecount,
		totalamount,isappliedforsignedcopy,documentstatusid,submittedby,submitteddatetime,preparedby,prepareddatetime,signedby,
		signeddatetime,appliedsignedcopy,comparedby,compareddatetime,certificatenumber,accepteddatetime,marriagetypeid,firmtypeid,applicationnumber,
		signedform22,gscno,k1k2_flag,inserteddatetime,isprior2003,refusalremarks,isrefused,finalregistrationnumber,isquicksearch
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.ccid,old.ccnumber,old.ccdate,old.userid,old.documenttype,old.kaveridrocode,old.kaverisrocode,old.documentnumber,old.booktype,old.yearofregistration,old.pagecount,
		old.totalamount,old.isappliedforsignedcopy,old.documentstatusid,old.submittedby,old.submitteddatetime,old.preparedby,old.prepareddatetime,old.signedby,
		old.signeddatetime,old.appliedsignedcopy,old.comparedby,old.compareddatetime,old.certificatenumber,old.accepteddatetime,old.marriagetypeid,old.firmtypeid,old.applicationnumber,
		old.signedform22,old.gscno,old.k1k2_flag,old.inserteddatetime,old.isprior2003,old.refusalremarks,old.isrefused,old.finalregistrationnumber,old.isquicksearch); return new;	
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.cc_applicationdetails_audit
		( username ,	action ,	query , 
		ccid,ccnumber,ccdate,userid,documenttype,kaveridrocode,kaverisrocode,documentnumber,booktype,yearofregistration,pagecount,
		totalamount,isappliedforsignedcopy,documentstatusid,submittedby,submitteddatetime,preparedby,prepareddatetime,signedby,
		signeddatetime,appliedsignedcopy,comparedby,compareddatetime,certificatenumber,accepteddatetime,marriagetypeid,firmtypeid,applicationnumber,
		signedform22,gscno,k1k2_flag,inserteddatetime,isprior2003,refusalremarks,isrefused,finalregistrationnumber,isquicksearch
		)
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.ccid,old.ccnumber,old.ccdate,old.userid,old.documenttype,old.kaveridrocode,old.kaverisrocode,old.documentnumber,old.booktype,old.yearofregistration,old.pagecount,
		old.totalamount,old.isappliedforsignedcopy,old.documentstatusid,old.submittedby,old.submitteddatetime,old.preparedby,old.prepareddatetime,old.signedby,
		old.signeddatetime,old.appliedsignedcopy,old.comparedby,old.compareddatetime,old.certificatenumber,old.accepteddatetime,old.marriagetypeid,old.firmtypeid,old.applicationnumber,
		old.signedform22,old.gscno,old.k1k2_flag,old.inserteddatetime,old.isprior2003,old.refusalremarks,old.isrefused,old.finalregistrationnumber,old.isquicksearch); return old;
    
	elsif tg_op = 'INSERT' then
	insert into kavericdc.cc_applicationdetails_audit
		( username ,	action ,	query , 
		ccid,ccnumber,ccdate,userid,documenttype,kaveridrocode,kaverisrocode,documentnumber,booktype,yearofregistration,pagecount,
		totalamount,isappliedforsignedcopy,documentstatusid,submittedby,submitteddatetime,preparedby,prepareddatetime,signedby,
		signeddatetime,appliedsignedcopy,comparedby,compareddatetime,certificatenumber,accepteddatetime,marriagetypeid,firmtypeid,applicationnumber,
		signedform22,gscno,k1k2_flag,inserteddatetime,isprior2003,refusalremarks,isrefused,finalregistrationnumber,isquicksearch
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		new.ccid,new.ccnumber,new.ccdate,new.userid,new.documenttype,new.kaveridrocode,new.kaverisrocode,new.documentnumber,new.booktype,new.yearofregistration,new.pagecount,
		new.totalamount,new.isappliedforsignedcopy,new.documentstatusid,new.submittedby,new.submitteddatetime,new.preparedby,new.prepareddatetime,new.signedby,
		new.signeddatetime,new.appliedsignedcopy,new.comparedby,new.compareddatetime,new.certificatenumber,new.accepteddatetime,new.marriagetypeid,new.firmtypeid,new.applicationnumber,
		new.signedform22,new.gscno,new.k1k2_flag,new.inserteddatetime,new.isprior2003,new.refusalremarks,new.isrefused,new.finalregistrationnumber,new.isquicksearch); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_cc_applicationdetails_audit() OWNER TO csgadmin;

--
-- Name: fn_delete_test_data(character varying); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_delete_test_data(_applicationnumber character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$

begin
	--delete from kaveri.applicationaudit where applicationnumber = _applicationnumber;
	
	delete from kaveri.propertybankdetails where documentid in(
    select documentid from kaveri.documentmaster where applicationnumber = _applicationnumber);
	
	delete from kaveri.documentmaster where applicationnumber = _applicationnumber;

	delete from kaveri.feesrequired where applicationnumber = _applicationnumber;

	delete from kaveri.partyinfo where applicationnumber = _applicationnumber;

	delete from kaveri.propertymaster where applicationnumber = _applicationnumber;
	
	delete from kaveri.propertyschedules where applicationnumber = _applicationnumber;

	delete from kaveri.witnessinfo where applicationnumber = _applicationnumber;

	delete from kaveri.partyschedules where applicationnumber = _applicationnumber;

	delete from kaveri.applicationaudit where applicationnumber = _applicationnumber;

	delete from kaveri.applicationreviewdetails where applicationnumber = _applicationnumber;

    delete from kaveri.val_agriculturedetails where valuationid in ( 
	select valid from kaveri.valuationdetails where applicationnumber = _applicationnumber);

	delete from kaveri.val_annexuredetails where valuationid in ( 
	select valid from kaveri.valuationdetails where applicationnumber = _applicationnumber);

	delete from kaveri.valuationdetails where applicationnumber = _applicationnumber;

	delete from kaveri.slottxn where applicationnumber = _applicationnumber;

	delete from kaveri.applicantapplicationdetails where applicationnumber = _applicationnumber;

return _applicationnumber;

end;
$$;


ALTER FUNCTION kavericdc.fn_delete_test_data(_applicationnumber character varying) OWNER TO csgadmin;

--
-- Name: fn_departmentusers_audit(); Type: FUNCTION; Schema: kavericdc; Owner: postgres
--

CREATE FUNCTION kavericdc.fn_departmentusers_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
        insert into kavericdc.departmentusers_audit 
		(username,"action",query,
		userid,srocode,loginname,firstname,middlename,lastname,doj,designationid,emailid,mobileno,serviceflag,serviceexpdate,passwd,usertype,periodfrom,periodto,bioauhreq,digiverifyreq,usrtype,crtusr,crtdate,joininglocation,houseno_per,buildingname_per,streetname_per,statecode_per,villagecode_per,districtcode_per,pincode_per,preferaddressis_per,houseno_curr,buildingname_curr,streetname_curr,statecode_curr,villagecode_curr,districtcode_curr,pincode_curr,emergencycontact,uploadphoto,pan,status,lstupdusrid,lstupddate,k1k2_flag,officeid,kgid,createdby,employeetypeid,districtcode,groupid,isactive,isdro
		)
		
		values(current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.userid,old.srocode,old.loginname,old.firstname,old.middlename,old.lastname,old.doj,old.designationid,old.emailid,old.mobileno,old.serviceflag,old.serviceexpdate,old.passwd,old.usertype,old.periodfrom,old.periodto,old.bioauhreq,old.digiverifyreq,old.usrtype,old.crtusr,old.crtdate,old.joininglocation,old.houseno_per,old.buildingname_per,old.streetname_per,old.statecode_per,old.villagecode_per,old.districtcode_per,old.pincode_per,old.preferaddressis_per,old.houseno_curr,old.buildingname_curr,old.streetname_curr,old.statecode_curr,old.villagecode_curr,old.districtcode_curr,old.pincode_curr,old.emergencycontact,old.uploadphoto,old.pan,old.status,old.lstupdusrid,old.lstupddate,old.k1k2_flag,old.officeid,old.kgid,old.createdby,old.employeetypeid,old.districtcode,old.groupid,old.isactive,old.isdro
		); return new;	
		
	elsif tg_op = 'DELETE' then
		insert into kavericdc.departmentusers_audit 
		(username,action,query,
		userid,srocode,loginname,firstname,middlename,lastname,doj,designationid,emailid,mobileno,serviceflag,serviceexpdate,passwd,usertype,periodfrom,periodto,bioauhreq,digiverifyreq,usrtype,crtusr,crtdate,joininglocation,houseno_per,buildingname_per,streetname_per,statecode_per,villagecode_per,districtcode_per,pincode_per,preferaddressis_per,houseno_curr,buildingname_curr,streetname_curr,statecode_curr,villagecode_curr,districtcode_curr,pincode_curr,emergencycontact,uploadphoto,pan,status,lstupdusrid,lstupddate,k1k2_flag,officeid,kgid,createdby,employeetypeid,districtcode,groupid,isactive,isdro
		)
		
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.userid,old.srocode,old.loginname,old.firstname,old.middlename,old.lastname,old.doj,old.designationid,old.emailid,old.mobileno,old.serviceflag,old.serviceexpdate,old.passwd,old.usertype,old.periodfrom,old.periodto,old.bioauhreq,old.digiverifyreq,old.usrtype,old.crtusr,old.crtdate,old.joininglocation,old.houseno_per,old.buildingname_per,old.streetname_per,old.statecode_per,old.villagecode_per,old.districtcode_per,old.pincode_per,old.preferaddressis_per,old.houseno_curr,old.buildingname_curr,old.streetname_curr,old.statecode_curr,old.villagecode_curr,old.districtcode_curr,old.pincode_curr,old.emergencycontact,old.uploadphoto,old.pan,old.status,old.lstupdusrid,old.lstupddate,old.k1k2_flag,old.officeid,old.kgid,old.createdby,old.employeetypeid,old.districtcode,old.groupid,old.isactive,old.isdro
		); return old;
    
	elsif tg_op = 'INSERT' then
	
		insert into kavericdc.departmentusers_audit 
		(username,action,query,
		userid,srocode,loginname,firstname,middlename,lastname,doj,designationid,emailid,mobileno,serviceflag,serviceexpdate,passwd,usertype,periodfrom,periodto,bioauhreq,digiverifyreq,usrtype,crtusr,crtdate,joininglocation,houseno_per,buildingname_per,streetname_per,statecode_per,villagecode_per,districtcode_per,pincode_per,preferaddressis_per,houseno_curr,buildingname_curr,streetname_curr,statecode_curr,villagecode_curr,districtcode_curr,pincode_curr,emergencycontact,uploadphoto,pan,status,lstupdusrid,lstupddate,k1k2_flag,officeid,kgid,createdby,employeetypeid,districtcode,groupid,isactive,isdro
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		new.userid,new.srocode,new.loginname,new.firstname,new.middlename,new.lastname,new.doj,new.designationid,new.emailid,new.mobileno,new.serviceflag,new.serviceexpdate,new.passwd,new.usertype,new.periodfrom,new.periodto,new.bioauhreq,new.digiverifyreq,new.usrtype,new.crtusr,new.crtdate,new.joininglocation,new.houseno_per,new.buildingname_per,new.streetname_per,new.statecode_per,new.villagecode_per,new.districtcode_per,new.pincode_per,new.preferaddressis_per,new.houseno_curr,new.buildingname_curr,new.streetname_curr,new.statecode_curr,new.villagecode_curr,new.districtcode_curr,new.pincode_curr,new.emergencycontact,new.uploadphoto,new.pan,new.status,new.lstupdusrid,new.lstupddate,new.k1k2_flag,new.officeid,new.kgid,new.createdby,new.employeetypeid,new.districtcode,new.groupid,new.isactive,new.isdro
		); return new;
	
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_departmentusers_audit() OWNER TO postgres;

--
-- Name: fn_documentmaster_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_documentmaster_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
        insert into kavericdc.documentmaster_audit 
		(
    username, action ,query ,documentid,   srocode,   bookid,   stamparticlecode,   regarticlecode,   documentnumber,   
	finalregistrationnumber,   presentdatetime,   executiondatetime,   dateofstamp,   stamp1datetime,   stamp2datetime,   
	stamp3datetime,   stamp4datetime,   stamp5datetime,   withdrawaldate,   pagecount,   index2shera,   isvisited,   isfiling,   
	ispending,   isscanned,   isrefused,   ispaymentofmoney,   isadjudicated,   iswithdrawn,   refusaldate,   refusalreason,   remarksbyuser,   
	remarksbysystem,   correctionreference,   olddocreference,   adjudicationdetails,   cdnumber,   isxmltransferredtobhoomi,   uid,   
	pendingdocumentnumber,   istransmitted,   isphotothumbtransmitted,   inserteddatetime,   initialtransmitted,   considerationamount,   requiredstampduty,   
	paidstampduty,   documentstatus,   applicationnumber,   verified,   issroapproved,   deedattachpath,   ispaymentdetails,   isuploaddocuments,   
	uploaddocdatetime,   registrationdatetime,   isregistrationevaluation,   uploaddocdeedpath,   uploaddocannexurepath,   docsubmitiondate,   
	lstupddate,   isregistrationaccepted,   isprintsummary,   isprintendorsement,   isgenerateec,   isdigitalsigned,   isregistrationcompleted,   
	gscno,   uploadsummarydocpath,   partypaymentdetails,   isscancompleted,   isundervaluation,   
	k1k2_flag,   withdrawfilepath,   withdrawdocument,   ackdatetime,   ackuser,lateappearancepartyid,uploadthumbregisterpath,isdigitallyexecuted,issignpageappended,isthumbregisterdocsigned,ispendingnoteappended,
	isendorsepagenumber,islegacydocscanned
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
	 old.documentid,   old.srocode,   old.bookid,   old.stamparticlecode,   old.regarticlecode,   old.documentnumber,   
	old.finalregistrationnumber,   old.presentdatetime,   old.executiondatetime,   old.dateofstamp,   old.stamp1datetime,   
	old.stamp2datetime,   old.stamp3datetime,   old.stamp4datetime,   old.stamp5datetime,   old.withdrawaldate,   old.pagecount,   
	old.index2shera,   old.isvisited,   old.isfiling,   old.ispending,   old.isscanned,   old.isrefused,   old.ispaymentofmoney,   
	old.isadjudicated,   old.iswithdrawn,   old.refusaldate,   old.refusalreason,   old.remarksbyuser,   old.remarksbysystem,   
	old.correctionreference,   old.olddocreference,   old.adjudicationdetails,   old.cdnumber,   old.isxmltransferredtobhoomi,   
	old.uid,   old.pendingdocumentnumber,   old.istransmitted,   old.isphotothumbtransmitted,   old.inserteddatetime,   
	old.initialtransmitted,   old.considerationamount,   old.requiredstampduty,   old.paidstampduty,   old.documentstatus,   
	old.applicationnumber,   old.verified,   old.issroapproved,   old.deedattachpath,   old.ispaymentdetails,   
	old.isuploaddocuments,   old.uploaddocdatetime,   old.registrationdatetime,   old.isregistrationevaluation,   
	old.uploaddocdeedpath,   old.uploaddocannexurepath,   old.docsubmitiondate,   old.lstupddate,   
	old.isregistrationaccepted,   old.isprintsummary,   old.isprintendorsement,   old.isgenerateec,   old.isdigitalsigned,   
	old.isregistrationcompleted,   old.gscno,   old.uploadsummarydocpath,   old.partypaymentdetails,   old.isscancompleted,   
	old.isundervaluation,   old.k1k2_flag,   old.withdrawfilepath,   old.withdrawdocument,   old.ackdatetime, old.ackuser,old.lateappearancepartyid,old.uploadthumbregisterpath
	,old.isdigitallyexecuted,old.issignpageappended,old.isthumbregisterdocsigned,old.ispendingnoteappended,old.isendorsepagenumber,old.islegacydocscanned
	); return new;	
		
	elsif tg_op = 'DELETE' then
       insert into kavericdc.documentmaster_audit 
		(
    username ,	action , query ,documentid,   srocode,   bookid,   stamparticlecode,   regarticlecode,   documentnumber,   
	finalregistrationnumber,   presentdatetime,   executiondatetime,   dateofstamp,   stamp1datetime,   stamp2datetime,   
	stamp3datetime,   stamp4datetime,   stamp5datetime,   withdrawaldate,   pagecount,   index2shera,   isvisited,   isfiling,   
	ispending,   isscanned,   isrefused,   ispaymentofmoney,   isadjudicated,   iswithdrawn,   refusaldate,   refusalreason,   remarksbyuser,   
	remarksbysystem,   correctionreference,   olddocreference,   adjudicationdetails,   cdnumber,   isxmltransferredtobhoomi,   uid,   
	pendingdocumentnumber,   istransmitted,   isphotothumbtransmitted,   inserteddatetime,   initialtransmitted,   considerationamount,   requiredstampduty,   
	paidstampduty,   documentstatus,   applicationnumber,   verified,   issroapproved,   deedattachpath,   ispaymentdetails,   isuploaddocuments,   
	uploaddocdatetime,   registrationdatetime,   isregistrationevaluation,   uploaddocdeedpath,   uploaddocannexurepath,   docsubmitiondate,   
	lstupddate,   isregistrationaccepted,   isprintsummary,   isprintendorsement,   isgenerateec,   isdigitalsigned,   isregistrationcompleted,   
	gscno,   uploadsummarydocpath,   partypaymentdetails,   isscancompleted,   isundervaluation,   
	k1k2_flag,   withdrawfilepath,   withdrawdocument,   ackdatetime,   ackuser,lateappearancepartyid,uploadthumbregisterpath,isdigitallyexecuted,issignpageappended,isthumbregisterdocsigned,ispendingnoteappended,
	isendorsepagenumber,islegacydocscanned
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
	 old.documentid,   old.srocode,   old.bookid,   old.stamparticlecode,   old.regarticlecode,   old.documentnumber,   
	old.finalregistrationnumber,   old.presentdatetime,   old.executiondatetime,   old.dateofstamp,   old.stamp1datetime,   
	old.stamp2datetime,   old.stamp3datetime,   old.stamp4datetime,   old.stamp5datetime,   old.withdrawaldate,   old.pagecount,   
	old.index2shera,   old.isvisited,   old.isfiling,   old.ispending,   old.isscanned,   old.isrefused,   old.ispaymentofmoney,   
	old.isadjudicated,   old.iswithdrawn,   old.refusaldate,   old.refusalreason,   old.remarksbyuser,   old.remarksbysystem,   
	old.correctionreference,   old.olddocreference,   old.adjudicationdetails,   old.cdnumber,   old.isxmltransferredtobhoomi,   
	old.uid,   old.pendingdocumentnumber,   old.istransmitted,   old.isphotothumbtransmitted,   old.inserteddatetime,   
	old.initialtransmitted,   old.considerationamount,   old.requiredstampduty,   old.paidstampduty,   old.documentstatus,   
	old.applicationnumber,   old.verified,   old.issroapproved,   old.deedattachpath,   old.ispaymentdetails,   
	old.isuploaddocuments,   old.uploaddocdatetime,   old.registrationdatetime,   old.isregistrationevaluation,   
	old.uploaddocdeedpath,   old.uploaddocannexurepath,   old.docsubmitiondate,   old.lstupddate,   
	old.isregistrationaccepted,   old.isprintsummary,   old.isprintendorsement,   old.isgenerateec,   old.isdigitalsigned,   
	old.isregistrationcompleted,   old.gscno,   old.uploadsummarydocpath,   old.partypaymentdetails,   old.isscancompleted,   
	old.isundervaluation,   old.k1k2_flag,   old.withdrawfilepath,   old.withdrawdocument,   old.ackdatetime,   old.ackuser,old.lateappearancepartyid,old.uploadthumbregisterpath
	,old.isdigitallyexecuted,old.issignpageappended,old.isthumbregisterdocsigned,old.ispendingnoteappended,old.isendorsepagenumber,old.islegacydocscanned
	); return old;
    
	elsif tg_op = 'INSERT' then
	
	insert into kavericdc.documentmaster_audit 
		(
    username ,	action ,  query ,documentid,   srocode,   bookid,   stamparticlecode,   regarticlecode,   documentnumber,   
	finalregistrationnumber,   presentdatetime,   executiondatetime,   dateofstamp,   stamp1datetime,   stamp2datetime,   
	stamp3datetime,   stamp4datetime,   stamp5datetime,   withdrawaldate,   pagecount,   index2shera,   isvisited,   isfiling,   
	ispending,   isscanned,   isrefused,   ispaymentofmoney,   isadjudicated,   iswithdrawn,   refusaldate,   refusalreason,   remarksbyuser,   
	remarksbysystem,   correctionreference,   olddocreference,   adjudicationdetails,   cdnumber,   isxmltransferredtobhoomi,   uid,   
	pendingdocumentnumber,   istransmitted,   isphotothumbtransmitted,   inserteddatetime,   initialtransmitted,   considerationamount,   requiredstampduty,   
	paidstampduty,   documentstatus,   applicationnumber,   verified,   issroapproved,   deedattachpath,   ispaymentdetails,   isuploaddocuments,   
	uploaddocdatetime,   registrationdatetime,   isregistrationevaluation,   uploaddocdeedpath,   uploaddocannexurepath,   docsubmitiondate,   
	lstupddate,   isregistrationaccepted,   isprintsummary,   isprintendorsement,   isgenerateec,   isdigitalsigned,   isregistrationcompleted,   
	gscno,   uploadsummarydocpath,   partypaymentdetails,   isscancompleted,   isundervaluation,   
	k1k2_flag,   withdrawfilepath,   withdrawdocument,   ackdatetime,   ackuser,lateappearancepartyid,uploadthumbregisterpath,isdigitallyexecuted,issignpageappended,isthumbregisterdocsigned,ispendingnoteappended,
	isendorsepagenumber,islegacydocscanned
	)
        	 values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
	new.documentid,   new.srocode,   new.bookid,   new.stamparticlecode,   new.regarticlecode,   new.documentnumber,   
	new.finalregistrationnumber,   new.presentdatetime,   new.executiondatetime,   new.dateofstamp,   new.stamp1datetime,   
	new.stamp2datetime,   new.stamp3datetime,   new.stamp4datetime,   new.stamp5datetime,   new.withdrawaldate,   new.pagecount,   
	new.index2shera,   new.isvisited,   new.isfiling,   new.ispending,   new.isscanned,   new.isrefused,   new.ispaymentofmoney,   
	new.isadjudicated,   new.iswithdrawn,   new.refusaldate,   new.refusalreason,   new.remarksbyuser,   new.remarksbysystem,   
	new.correctionreference,   new.olddocreference,   new.adjudicationdetails,   new.cdnumber,   new.isxmltransferredtobhoomi,   
	new.uid,   new.pendingdocumentnumber,   new.istransmitted,   new.isphotothumbtransmitted,   new.inserteddatetime,   
	new.initialtransmitted,   new.considerationamount,   new.requiredstampduty,   new.paidstampduty,   new.documentstatus,   
	new.applicationnumber,   new.verified,   new.issroapproved,   new.deedattachpath,   new.ispaymentdetails,   
	new.isuploaddocuments,   new.uploaddocdatetime,   new.registrationdatetime,   new.isregistrationevaluation,   
	new.uploaddocdeedpath,   new.uploaddocannexurepath,   new.docsubmitiondate,   new.lstupddate,   
	new.isregistrationaccepted,   new.isprintsummary,   new.isprintendorsement,   new.isgenerateec,   new.isdigitalsigned,   
	new.isregistrationcompleted,   new.gscno,   new.uploadsummarydocpath,   new.partypaymentdetails,   new.isscancompleted,   
	new.isundervaluation,   new.k1k2_flag,   new.withdrawfilepath,   new.withdrawdocument,   new.ackdatetime,   new.ackuser,new.lateappearancepartyid,new.uploadthumbregisterpath
	,new.isdigitallyexecuted,new.issignpageappended,new.isthumbregisterdocsigned,new.ispendingnoteappended,new.isendorsepagenumber,new.islegacydocscanned
	); return new;
	
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_documentmaster_audit() OWNER TO csgadmin;

--
-- Name: fn_eaasti_eswatuxmllog_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.eaasti_eswatuxmllog_audit
		( username ,	action ,	query , 
		logid,	documentid ,propertyid ,pid  ,"xml"  ,srocode  ,inserteddatetime  ,	k1k2_flag  
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.logid,old.documentid,old.propertyid,old.pid,old."xml" ,old.srocode ,old.inserteddatetime ,old.k1k2_flag  ); return new;	
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.eaasti_eswatuxmllog_audit
		( username ,	action ,	query , 
		logid,	documentid ,propertyid ,pid  ,"xml"  ,srocode  ,inserteddatetime  ,	k1k2_flag  
		)
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.logid,old.documentid,old.propertyid,old.pid,old."xml" ,old.srocode ,old.inserteddatetime ,old.k1k2_flag); return old;
    
	elsif tg_op = 'INSERT' then
	insert into kavericdc.eaasti_eswatuxmllog_audit
		( username ,	action ,	query , 
		logid,	documentid ,propertyid ,pid  ,"xml"  ,srocode  ,inserteddatetime  ,	k1k2_flag  
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		new.logid,new.documentid,new.propertyid,new.pid,new."xml" ,new.srocode ,new.inserteddatetime ,new.k1k2_flag); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() OWNER TO csgadmin;

--
-- Name: fn_ecapplicationdetals_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_ecapplicationdetals_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
        insert into kavericdc.ec_applicationdetails_audit
		(
    username, action ,query, ecid,ecnumber,certificatenumber,ecdate,userid,searchfromdate,searchtodate,kaveridrocode,kaverisrocode,kaverivillagecode,kaverihoblicode,pagecount,totalamount,submittedby,submitteddatetime,acceptedby,acceptedon,documentstatusid,preparedby,prepareddatetime,signedby,signeddatetime,appliedsignedcopy,comparedby,compareddatetime,eastboundary,westboundary,northboundary,southboundary,easttowest,northtosouth,remarktoreprepareec,area,propertydescription,measurementunitid,hectare,acre,gunta,cents,partyname,isnamesearch,ispropertysearch,isdocviewable,applicationnumber,easttowestmeasurement,northtosouthmeasurement,propertytypeid,signedform22,gscno,k1k2_flag,inserteddatetime,reason,isappliedbydept,isbefore2004,refusalremarks,isrefused

	)
		
	 values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.ecid,old.ecnumber,old.certificatenumber,old.ecdate,old.userid,old.searchfromdate,old.searchtodate,old.kaveridrocode,old.kaverisrocode,old.kaverivillagecode,old.kaverihoblicode,old.pagecount,old.totalamount,old.submittedby,old.submitteddatetime,old.acceptedby,old.acceptedon,old.documentstatusid,old.preparedby,old.prepareddatetime,old.signedby,old.signeddatetime,old.appliedsignedcopy,old.comparedby,old.compareddatetime,old.eastboundary,old.westboundary,old.northboundary,old.southboundary,old.easttowest,old.northtosouth,old.remarktoreprepareec,old.area,old.propertydescription,old.measurementunitid,old.hectare,old.acre,old.gunta,old.cents,old.partyname,old.isnamesearch,old.ispropertysearch,old.isdocviewable,old.applicationnumber,old.easttowestmeasurement,old.northtosouthmeasurement,old.propertytypeid,old.signedform22,old.gscno,old.k1k2_flag,old.inserteddatetime,old.reason,old.isappliedbydept,old.isbefore2004,old.refusalremarks,old.isrefused
	); return new;	
		
	elsif tg_op = 'DELETE' then
       insert into kavericdc.ec_applicationdetails_audit 
		(
    username ,	action , query ,ecid,ecnumber,certificatenumber,ecdate,userid,searchfromdate,searchtodate,kaveridrocode,kaverisrocode,kaverivillagecode,kaverihoblicode,pagecount,totalamount,submittedby,submitteddatetime,acceptedby,acceptedon,documentstatusid,preparedby,prepareddatetime,signedby,signeddatetime,appliedsignedcopy,comparedby,compareddatetime,eastboundary,westboundary,northboundary,southboundary,easttowest,northtosouth,remarktoreprepareec,area,propertydescription,measurementunitid,hectare,acre,gunta,cents,partyname,isnamesearch,ispropertysearch,isdocviewable,applicationnumber,easttowestmeasurement,northtosouthmeasurement,propertytypeid,signedform22,gscno,k1k2_flag,inserteddatetime,reason,isappliedbydept,isbefore2004,refusalremarks,isrefused

	)
		
	 values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
	 old.ecid,old.ecnumber,old.certificatenumber,old.ecdate,old.userid,old.searchfromdate,old.searchtodate,old.kaveridrocode,old.kaverisrocode,old.kaverivillagecode,old.kaverihoblicode,old.pagecount,old.totalamount,old.submittedby,old.submitteddatetime,old.acceptedby,old.acceptedon,old.documentstatusid,old.preparedby,old.prepareddatetime,old.signedby,old.signeddatetime,old.appliedsignedcopy,old.comparedby,old.compareddatetime,old.eastboundary,old.westboundary,old.northboundary,old.southboundary,old.easttowest,old.northtosouth,old.remarktoreprepareec,old.area,old.propertydescription,old.measurementunitid,old.hectare,old.acre,old.gunta,old.cents,old.partyname,old.isnamesearch,old.ispropertysearch,old.isdocviewable,old.applicationnumber,old.easttowestmeasurement,old.northtosouthmeasurement,old.propertytypeid,old.signedform22,old.gscno,old.k1k2_flag,old.inserteddatetime,old.reason,old.isappliedbydept,old.isbefore2004,old.refusalremarks,old.isrefused
	); return old;
    
	elsif tg_op = 'INSERT' then
	
	insert into kavericdc.ec_applicationdetails_audit
		(
    username ,	action ,  query ,ecid,ecnumber,certificatenumber,ecdate,userid,searchfromdate,searchtodate,kaveridrocode,kaverisrocode,kaverivillagecode,kaverihoblicode,pagecount,totalamount,submittedby,submitteddatetime,acceptedby,acceptedon,documentstatusid,preparedby,prepareddatetime,signedby,signeddatetime,appliedsignedcopy,comparedby,compareddatetime,eastboundary,westboundary,northboundary,southboundary,easttowest,northtosouth,remarktoreprepareec,area,propertydescription,measurementunitid,hectare,acre,gunta,cents,partyname,isnamesearch,ispropertysearch,isdocviewable,applicationnumber,easttowestmeasurement,northtosouthmeasurement,propertytypeid,signedform22,gscno,k1k2_flag,inserteddatetime,reason,isappliedbydept,isbefore2004,refusalremarks,isrefused
	)
        	 values (current_user::text||' 2'||session_user::text, 'Inserted', current_query()
			 ,new.ecid,new.ecnumber,new.certificatenumber,new.ecdate,new.userid,new.searchfromdate,new.searchtodate,new.kaveridrocode,new.kaverisrocode,new.kaverivillagecode,new.kaverihoblicode,new.pagecount,new.totalamount,new.submittedby,new.submitteddatetime,new.acceptedby,new.acceptedon,new.documentstatusid,new.preparedby,new.prepareddatetime,new.signedby,new.signeddatetime,new.appliedsignedcopy,new.comparedby,new.compareddatetime,new.eastboundary,new.westboundary,new.northboundary,new.southboundary,new.easttowest,new.northtosouth,new.remarktoreprepareec,new.area,new.propertydescription,new.measurementunitid,new.hectare,new.acre,new.gunta,new.cents,new.partyname,new.isnamesearch,new.ispropertysearch,new.isdocviewable,new.applicationnumber,new.easttowestmeasurement,new.northtosouthmeasurement,new.propertytypeid,new.signedform22,new.gscno,new.k1k2_flag,new.inserteddatetime,new.reason,new.isappliedbydept,new.isbefore2004,new.refusalremarks,new.isrefused
	); return new;
	
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_ecapplicationdetals_audit() OWNER TO csgadmin;

--
-- Name: fn_feesrequired_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_feesrequired_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.feesrequired_audit
		( username ,	action ,	query , 
		documentid,feerulecode,isexempted,exemptdescription,isactive,feecalculationstring,srocode,
		isonline,amountrequired,applicationnumber,propertyid,lastupdateddate,exemtype,exemamount,exemdocpath,
		denodocpath,sfdaamountrequired,sroamountrequired,amountpaid,valuatiotypeid,sfdastamprule,srostamprule,
		regexemtype,regexemamount,paymentstatus,inserteddatetime,k1k2_flag,receiptid,undervaluationamount
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.documentid,   old.feerulecode,   old.isexempted,   old.exemptdescription,   old.isactive,   
		old.feecalculationstring,   old.srocode,   old.isonline,   old.amountrequired,   old.applicationnumber,   
		old.propertyid,   old.lastupdateddate,   old.exemtype,   old.exemamount,   old.exemdocpath,   old.denodocpath,   
		old.sfdaamountrequired,   old.sroamountrequired,   old.amountpaid,   old.valuatiotypeid,   old.sfdastamprule,   
		old.srostamprule,   old.regexemtype,   old.regexemamount,   old.paymentstatus,   
		old.inserteddatetime,   old.k1k2_flag,   old.receiptid,   old.undervaluationamount); return new;	
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.feesrequired_audit
		( username ,	action ,	query , 
		documentid,feerulecode,isexempted,exemptdescription,isactive,feecalculationstring,srocode,
		isonline,amountrequired,applicationnumber,propertyid,lastupdateddate,exemtype,exemamount,exemdocpath,
		denodocpath,sfdaamountrequired,sroamountrequired,amountpaid,valuatiotypeid,sfdastamprule,srostamprule,
		regexemtype,regexemamount,paymentstatus,inserteddatetime,k1k2_flag,receiptid,undervaluationamount
		)
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.documentid,   old.feerulecode,   old.isexempted,   old.exemptdescription,   old.isactive,   
		old.feecalculationstring,   old.srocode,   old.isonline,   old.amountrequired,   old.applicationnumber,   
		old.propertyid,   old.lastupdateddate,   old.exemtype,   old.exemamount,   old.exemdocpath,   old.denodocpath,   
		old.sfdaamountrequired,   old.sroamountrequired,   old.amountpaid,   old.valuatiotypeid,   old.sfdastamprule,   
		old.srostamprule,   old.regexemtype,   old.regexemamount,   old.paymentstatus,   
		old.inserteddatetime,   old.k1k2_flag,   old.receiptid,   old.undervaluationamount); return old;
    
	elsif tg_op = 'INSERT' then
	insert into kavericdc.feesrequired_audit
		( username ,	action ,	query , 
		documentid,feerulecode,isexempted,exemptdescription,isactive,feecalculationstring,srocode,
		isonline,amountrequired,applicationnumber,propertyid,lastupdateddate,exemtype,exemamount,exemdocpath,
		denodocpath,sfdaamountrequired,sroamountrequired,amountpaid,valuatiotypeid,sfdastamprule,srostamprule,
		regexemtype,regexemamount,paymentstatus,inserteddatetime,k1k2_flag,receiptid,undervaluationamount
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		new.documentid,   new.feerulecode,   new.isexempted,   new.exemptdescription,   new.isactive,   
		new.feecalculationstring,   new.srocode,   new.isonline,   new.amountrequired,   new.applicationnumber,   
		new.propertyid,   new.lastupdateddate,   new.exemtype,   new.exemamount,   new.exemdocpath,   new.denodocpath,   
		new.sfdaamountrequired,   new.sroamountrequired,   new.amountpaid,   new.valuatiotypeid,   new.sfdastamprule,   
		new.srostamprule,   new.regexemtype,   new.regexemamount,   new.paymentstatus,   
		new.inserteddatetime,   new.k1k2_flag,   new.receiptid,   new.undervaluationamount); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_feesrequired_audit() OWNER TO csgadmin;

--
-- Name: fn_insert_mdm_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_insert_mdm_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    if tg_op = 'UPDATE' then
       /* insert into kavericdc.mdm_audit_table (table_name, user_name, action, old_values, new_values, updated_cols, query)
        values (tg_table_name::text, current_user::text||' 2'||session_user::text, 'Updated', kaveri.hstore(old.*), kaveri.hstore(new.*),
               akeys(kaveri.hstore(new.*) - kaveri.hstore(old.*)), current_query()); */
	 insert into kavericdc.mdm_audit_table (table_name, user_name, action, old_values, new_values, query)
        values (tg_table_name::text, current_user::text||' 2'||session_user::text, 'Updated', kaveri.hstore(old.*), kaveri.hstore(new.*),
               current_query());
        return new;
    elsif tg_op = 'DELETE' then
        insert into kavericdc.mdm_audit_table (table_name, user_name, action, old_values, query)
        values (tg_table_name::text, current_user::text||' 2'||session_user::text, 'Deleted', kaveri.hstore(old.*), current_query());
        return old;
    elsif tg_op = 'INSERT' then
        insert into kavericdc.mdm_audit_table (table_name, user_name, action, new_values, query)
        values (tg_table_name::text, current_user::text, 'Inserted', kaveri.hstore(new.*), current_query());
        return new;
	
    end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_insert_mdm_audit() OWNER TO csgadmin;

--
-- Name: fn_minutebook_data_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_minutebook_data_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.minutebook_data_audit
		( username ,	action ,	query , 
		docid,applicationnumber,remarks,issystem,minutedate,srocode,reasonid,
		remark_comment,inserteddatetime,k1k2_flag,private_remark,dr_order_number,dr_order_filepath,ispendingdocument,pendingregistrationnumber,
		isbefore2003
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.docid,   old.applicationnumber,   old.remarks,   old.issystem,   old.minutedate,   
		old.srocode,   old.reasonid,   old.remark_comment,   old.inserteddatetime,   old.k1k2_flag,   
		old.private_remark,   old.dr_order_number,   old.dr_order_filepath,   old.ispendingdocument,   old.pendingregistrationnumber,   old.isbefore2003
		); return new;	
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.minutebook_data_audit
		( username ,	action ,	query , 
		docid,applicationnumber,remarks,issystem,minutedate,srocode,reasonid,
		remark_comment,inserteddatetime,k1k2_flag,private_remark,dr_order_number,dr_order_filepath,ispendingdocument,pendingregistrationnumber,
		isbefore2003
		)
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.docid,   old.applicationnumber,   old.remarks,   old.issystem,   old.minutedate,   
		old.srocode,   old.reasonid,   old.remark_comment,   old.inserteddatetime,   old.k1k2_flag,   
		old.private_remark,   old.dr_order_number,   old.dr_order_filepath,   old.ispendingdocument,   old.pendingregistrationnumber,   old.isbefore2003
		); return old;
    
	elsif tg_op = 'INSERT' then
	insert into kavericdc.minutebook_data_audit
		( username ,	action ,	query , 
		docid,applicationnumber,remarks,issystem,minutedate,srocode,reasonid,
		remark_comment,inserteddatetime,k1k2_flag,private_remark,dr_order_number,dr_order_filepath,ispendingdocument,pendingregistrationnumber,
		isbefore2003
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		new.docid,new.applicationnumber,new.remarks,new.issystem,new.minutedate,   
		new.srocode,new.reasonid,new.remark_comment,new.inserteddatetime,new.k1k2_flag,   
		new.private_remark,new.dr_order_number,new.dr_order_filepath,new.ispendingdocument
		,new.pendingregistrationnumber,new.isbefore2003); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_minutebook_data_audit() OWNER TO csgadmin;

--
-- Name: fn_partyinfo_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_partyinfo_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.partyinfo_audit
		( username ,	action ,	query , 
		partyid,  srocode,  documentid,  partytypeid,  firstname,  middlename,  lastname,  address,  age,  sex,  
		isexecutor,  ispresenter,  admissiondate,  aliasname,  correctedname,  relationship,  relativename,  
		epic,  pan,  phonenumber,  availableextacre,  availableextgunta,  availableextfgunta,  bincom,  category,  
		dateofdeath,  fingerid,  fingerverificationstatusid,  ispartofrtc,  landcode,  mainownerno,  ownerno,  
		partypoa,  photopath,  poaadmission,  poapresentation,  primaryseller,  profession,  restriction,  
		restrictiondescription,  restrictiontype,  section88exemption,  thumbmatchfailedreasonid,  
		thumbminutiae,  thumbpath,  totalextacre,  totalextgunta,  totalextfgunta,  transactextacre,  
		transactextgunta,  transactextfgunta,  volumename,  hasgpa,  isaua,  importedpartyparentid,  
		salutationid,  isorganization,  organizationid,  applicationnumber,  verified,  issroapproved,  
		districtcode,  talukcode,  hoblicode,  villagecode,  tanno,  yearofincorp,  orgpoaauthsignfname,  
		orgpoaauthsignmname,  orgpoaauthsignlname,  linkpartyid,  housenumber,  pin,  propertyid,  propertynumber,  
		idprooftypeid,  isconsentwitness,  isprivateattendance,  coveringletterno,  section88file,  
		isendorseprinted,  thumbremarks,  partyidreference,  inserteddatetime,  
		k1k2_flag,  ispartyrefused,  islateapperance,  duplicatepartyid,  isduplicate,
		presenternamee, isbiometricrefused, iscitizennotappeared,
		aadharhash, datetimeofconsent, nameasperaadhar, digilockerid, isdeptaadharvalidated, iscitizenaadharverified,
		aadhaar_decline_reason, aadhaardeclinereason, idcardhash,isdocumentexecuted,isendorsementsigned,isthumbregistersigned,namematchpercentage,ispartypanverified,
		vaultid,transactionnumber
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.partyid,  old.srocode,  old.documentid,  old.partytypeid,  old.firstname,  old.middlename,  old.lastname,  
		old.address,  old.age,  old.sex,  old.isexecutor,  old.ispresenter,  old.admissiondate,  old.aliasname,  old.correctedname,  old.relationship,  
		old.relativename,  old.epic,  old.pan,  old.phonenumber,  old.availableextacre,  old.availableextgunta,  old.availableextfgunta,  old.bincom,  
		old.category,  old.dateofdeath,  old.fingerid,  old.fingerverificationstatusid,  old.ispartofrtc,  old.landcode,  old.mainownerno,  old.ownerno,  
		old.partypoa,  old.photopath,  old.poaadmission,  old.poapresentation,  old.primaryseller,  old.profession,  old.restriction,  old.restrictiondescription,  
		old.restrictiontype,  old.section88exemption,  old.thumbmatchfailedreasonid,  old.thumbminutiae,  old.thumbpath,  old.totalextacre,  old.totalextgunta,  
		old.totalextfgunta,  old.transactextacre,  old.transactextgunta,  old.transactextfgunta,  old.volumename,  old.hasgpa,  old.isaua,  old.importedpartyparentid,  
		old.salutationid,  old.isorganization,  old.organizationid,  old.applicationnumber,  old.verified,  old.issroapproved,  old.districtcode,  old.talukcode,  
		old.hoblicode,  old.villagecode,  old.tanno,  old.yearofincorp,  old.orgpoaauthsignfname,  old.orgpoaauthsignmname,  old.orgpoaauthsignlname,  old.linkpartyid,  
		old.housenumber,  old.pin,  old.propertyid,  old.propertynumber,  old.idprooftypeid,  old.isconsentwitness,  old.isprivateattendance,  old.coveringletterno,  
		old.section88file,  old.isendorseprinted,  old.thumbremarks,  old.partyidreference,  old.inserteddatetime,  old.k1k2_flag,  old.ispartyrefused,  old.islateapperance,  
		old.duplicatepartyid,  old.isduplicate,
		old.presenternamee, old.isbiometricrefused, old.iscitizennotappeared,
		old.aadharhash, old.datetimeofconsent, old.nameasperaadhar, old.digilockerid, old.isdeptaadharvalidated, old.iscitizenaadharverified,
		old.aadhaar_decline_reason, old.aadhaardeclinereason, old.idcardhash,old.isdocumentexecuted,old.isendorsementsigned,old.isthumbregistersigned,old.namematchpercentage,old.ispartypanverified,old.vaultid,old.transactionnumber); return new;	
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.partyinfo_audit
		( username ,	action ,	query , 
		partyid,  srocode,  documentid,  partytypeid,  firstname,  middlename,  lastname,  address,  age,  sex,  
		isexecutor,  ispresenter,  admissiondate,  aliasname,  correctedname,  relationship,  relativename,  
		epic,  pan,  phonenumber,  availableextacre,  availableextgunta,  availableextfgunta,  bincom,  category,  
		dateofdeath,  fingerid,  fingerverificationstatusid,  ispartofrtc,  landcode,  mainownerno,  ownerno,  
		partypoa,  photopath,  poaadmission,  poapresentation,  primaryseller,  profession,  restriction,  
		restrictiondescription,  restrictiontype,  section88exemption,  thumbmatchfailedreasonid,  
		thumbminutiae,  thumbpath,  totalextacre,  totalextgunta,  totalextfgunta,  transactextacre,  
		transactextgunta,  transactextfgunta,  volumename,  hasgpa,  isaua,  importedpartyparentid,  
		salutationid,  isorganization,  organizationid,  applicationnumber,  verified,  issroapproved,  
		districtcode,  talukcode,  hoblicode,  villagecode,  tanno,  yearofincorp,  orgpoaauthsignfname,  
		orgpoaauthsignmname,  orgpoaauthsignlname,  linkpartyid,  housenumber,  pin,  propertyid,  propertynumber,  
		idprooftypeid,  isconsentwitness,  isprivateattendance,  coveringletterno,  section88file,  
		isendorseprinted,  thumbremarks,  partyidreference,  inserteddatetime,  
		k1k2_flag,  ispartyrefused,  islateapperance,  duplicatepartyid,  isduplicate,
		presenternamee, isbiometricrefused, iscitizennotappeared,
		aadharhash, datetimeofconsent, nameasperaadhar, digilockerid, isdeptaadharvalidated, iscitizenaadharverified,
		aadhaar_decline_reason, aadhaardeclinereason, idcardhash,isdocumentexecuted,isendorsementsigned,isthumbregistersigned,namematchpercentage,ispartypanverified,
		vaultid,transactionnumber
		)
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.partyid,  old.srocode,  old.documentid,  old.partytypeid,  old.firstname,  old.middlename,  old.lastname,  
		old.address,  old.age,  old.sex,  old.isexecutor,  old.ispresenter,  old.admissiondate,  old.aliasname,  old.correctedname,  old.relationship,  
		old.relativename,  old.epic,  old.pan,  old.phonenumber,  old.availableextacre,  old.availableextgunta,  old.availableextfgunta,  old.bincom,  
		old.category,  old.dateofdeath,  old.fingerid,  old.fingerverificationstatusid,  old.ispartofrtc,  old.landcode,  old.mainownerno,  old.ownerno,  
		old.partypoa,  old.photopath,  old.poaadmission,  old.poapresentation,  old.primaryseller,  old.profession,  old.restriction,  old.restrictiondescription,  
		old.restrictiontype,  old.section88exemption,  old.thumbmatchfailedreasonid,  old.thumbminutiae,  old.thumbpath,  old.totalextacre,  old.totalextgunta,  
		old.totalextfgunta,  old.transactextacre,  old.transactextgunta,  old.transactextfgunta,  old.volumename,  old.hasgpa,  old.isaua,  old.importedpartyparentid,  
		old.salutationid,  old.isorganization,  old.organizationid,  old.applicationnumber,  old.verified,  old.issroapproved,  old.districtcode,  old.talukcode,  
		old.hoblicode,  old.villagecode,  old.tanno,  old.yearofincorp,  old.orgpoaauthsignfname,  old.orgpoaauthsignmname,  old.orgpoaauthsignlname,  old.linkpartyid,  
		old.housenumber,  old.pin,  old.propertyid,  old.propertynumber,  old.idprooftypeid,  old.isconsentwitness,  old.isprivateattendance,  old.coveringletterno,  
		old.section88file,  old.isendorseprinted,  old.thumbremarks,  old.partyidreference,  old.inserteddatetime,  old.k1k2_flag,  old.ispartyrefused,  old.islateapperance,  
		old.duplicatepartyid,  old.isduplicate,
		old.presenternamee, old.isbiometricrefused, old.iscitizennotappeared,
		old.aadharhash, old.datetimeofconsent, old.nameasperaadhar, old.digilockerid, old.isdeptaadharvalidated, old.iscitizenaadharverified,
		old.aadhaar_decline_reason, old.aadhaardeclinereason, old.idcardhash,old.isdocumentexecuted,old.isendorsementsigned,old.isthumbregistersigned,old.namematchpercentage,old.ispartypanverified,old.vaultid,old.transactionnumber); return old;
    	
	elsif tg_op = 'INSERT' then
	insert into kavericdc.partyinfo_audit
		( username ,	action ,	query , 
		partyid,  srocode,  documentid,  partytypeid,  firstname,  middlename,  lastname,  address,  age,  sex,  
		isexecutor,  ispresenter,  admissiondate,  aliasname,  correctedname,  relationship,  relativename,  
		epic,  pan,  phonenumber,  availableextacre,  availableextgunta,  availableextfgunta,  bincom,  category,  
		dateofdeath,  fingerid,  fingerverificationstatusid,  ispartofrtc,  landcode,  mainownerno,  ownerno,  
		partypoa,  photopath,  poaadmission,  poapresentation,  primaryseller,  profession,  restriction,  
		restrictiondescription,  restrictiontype,  section88exemption,  thumbmatchfailedreasonid,  
		thumbminutiae,  thumbpath,  totalextacre,  totalextgunta,  totalextfgunta,  transactextacre,  
		transactextgunta,  transactextfgunta,  volumename,  hasgpa,  isaua,  importedpartyparentid,  
		salutationid,  isorganization,  organizationid,  applicationnumber,  verified,  issroapproved,  
		districtcode,  talukcode,  hoblicode,  villagecode,  tanno,  yearofincorp,  orgpoaauthsignfname,  
		orgpoaauthsignmname,  orgpoaauthsignlname,  linkpartyid,  housenumber,  pin,  propertyid,  propertynumber,  
		idprooftypeid,  isconsentwitness,  isprivateattendance,  coveringletterno,  section88file,  
		isendorseprinted,  thumbremarks,  partyidreference,  inserteddatetime,  
		k1k2_flag,  ispartyrefused,  islateapperance,  duplicatepartyid,  isduplicate,
		presenternamee, isbiometricrefused, iscitizennotappeared,
		aadharhash, datetimeofconsent, nameasperaadhar, digilockerid, isdeptaadharvalidated, iscitizenaadharverified,
		aadhaar_decline_reason, aadhaardeclinereason, idcardhash,isdocumentexecuted,isendorsementsigned,isthumbregistersigned,namematchpercentage,ispartypanverified
		,vaultid,transactionnumber
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		new.partyid,  new.srocode,  new.documentid,  new.partytypeid,  new.firstname,  new.middlename,  new.lastname,  
		new.address,  new.age,  new.sex,  new.isexecutor,  new.ispresenter,  new.admissiondate,  new.aliasname,  new.correctedname,  new.relationship,  
		new.relativename,  new.epic,  new.pan,  new.phonenumber,  new.availableextacre,  new.availableextgunta,  new.availableextfgunta,  new.bincom,  
		new.category,  new.dateofdeath,  new.fingerid,  new.fingerverificationstatusid,  new.ispartofrtc,  new.landcode,  new.mainownerno,  new.ownerno,  
		new.partypoa,  new.photopath,  new.poaadmission,  new.poapresentation,  new.primaryseller,  new.profession,  new.restriction,  new.restrictiondescription,  
		new.restrictiontype,  new.section88exemption,  new.thumbmatchfailedreasonid,  new.thumbminutiae,  new.thumbpath,  new.totalextacre,  new.totalextgunta,  
		new.totalextfgunta,  new.transactextacre,  new.transactextgunta,  new.transactextfgunta,  new.volumename,  new.hasgpa,  new.isaua,  new.importedpartyparentid,  
		new.salutationid,  new.isorganization,  new.organizationid,  new.applicationnumber,  new.verified,  new.issroapproved,  new.districtcode,  new.talukcode,  
		new.hoblicode,  new.villagecode,  new.tanno,  new.yearofincorp,  new.orgpoaauthsignfname,  new.orgpoaauthsignmname,  new.orgpoaauthsignlname,  new.linkpartyid,  
		new.housenumber,  new.pin,  new.propertyid,  new.propertynumber,  new.idprooftypeid,  new.isconsentwitness,  new.isprivateattendance,  new.coveringletterno,  
		new.section88file,  new.isendorseprinted,  new.thumbremarks,  new.partyidreference,  new.inserteddatetime,  new.k1k2_flag,  new.ispartyrefused,  new.islateapperance,  
		new.duplicatepartyid,  new.isduplicate,
		new.presenternamee, new.isbiometricrefused, new.iscitizennotappeared,
		new.aadharhash, new.datetimeofconsent, new.nameasperaadhar, new.digilockerid, new.isdeptaadharvalidated, new.iscitizenaadharverified,
		new.aadhaar_decline_reason, new.aadhaardeclinereason, new.idcardhash,new.isdocumentexecuted,new.isendorsementsigned,new.isthumbregistersigned,new.namematchpercentage,new.ispartypanverified,new.vaultid,new.transactionnumber); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_partyinfo_audit() OWNER TO csgadmin;

--
-- Name: fn_partyinfo_fruits_audit(); Type: FUNCTION; Schema: kavericdc; Owner: postgres
--

CREATE FUNCTION kavericdc.fn_partyinfo_fruits_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
	
	if exists(
		select applicationnumber from kaveri.fruitspushkaveripayload f where applicationnumber = old.applicationnumber) then

			if tg_op = 'DELETE' then
			insert into kavericdc.partyinfo_fruits_audit
				( username ,	action ,	query , 
				partyid,  srocode,  documentid,  partytypeid,  firstname,  middlename,  lastname,  address,  age,  sex,  
				isexecutor,  ispresenter,  admissiondate,  aliasname,  correctedname,  relationship,  relativename,  
				epic,  pan,  phonenumber,  availableextacre,  availableextgunta,  availableextfgunta,  bincom,  category,  
				dateofdeath,  fingerid,  fingerverificationstatusid,  ispartofrtc,  landcode,  mainownerno,  ownerno,  
				partypoa,  photopath,  poaadmission,  poapresentation,  primaryseller,  profession,  restriction,  
				restrictiondescription,  restrictiontype,  section88exemption,  thumbmatchfailedreasonid,  
				thumbminutiae,  thumbpath,  totalextacre,  totalextgunta,  totalextfgunta,  transactextacre,  
				transactextgunta,  transactextfgunta,  volumename,  hasgpa,  isaua,  importedpartyparentid,  
				salutationid,  isorganization,  organizationid,  applicationnumber,  verified,  issroapproved,  
				districtcode,  talukcode,  hoblicode,  villagecode,  tanno,  yearofincorp,  orgpoaauthsignfname,  
				orgpoaauthsignmname,  orgpoaauthsignlname,  linkpartyid,  housenumber,  pin,  propertyid,  propertynumber,  
				idprooftypeid,  isconsentwitness,  isprivateattendance,  coveringletterno,  section88file,  
				isendorseprinted,  thumbremarks,  partyidreference,  inserteddatetime,  
				k1k2_flag,  ispartyrefused,  islateapperance,  duplicatepartyid,  isduplicate,
				presenternamee, isbiometricrefused, iscitizennotappeared,
				aadharhash, datetimeofconsent, nameasperaadhar, digilockerid, isdeptaadharvalidated, iscitizenaadharverified,
				aadhaar_decline_reason, aadhaardeclinereason, idcardhash,isdocumentexecuted,isendorsementsigned,isthumbregistersigned,
				namematchpercentage,ispartypanverified,vaultid,transactionnumber
				)
				values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
				old.partyid,  old.srocode,  old.documentid,  old.partytypeid,  old.firstname,  old.middlename,  old.lastname,  
				old.address,  old.age,  old.sex,  old.isexecutor,  old.ispresenter,  old.admissiondate,  old.aliasname,  old.correctedname,  old.relationship,  
				old.relativename,  old.epic,  old.pan,  old.phonenumber,  old.availableextacre,  old.availableextgunta,  old.availableextfgunta,  old.bincom,  
				old.category,  old.dateofdeath,  old.fingerid,  old.fingerverificationstatusid,  old.ispartofrtc,  old.landcode,  old.mainownerno,  old.ownerno,  
				old.partypoa,  old.photopath,  old.poaadmission,  old.poapresentation,  old.primaryseller,  old.profession,  old.restriction,  old.restrictiondescription,  
				old.restrictiontype,  old.section88exemption,  old.thumbmatchfailedreasonid,  old.thumbminutiae,  old.thumbpath,  old.totalextacre,  old.totalextgunta,  
				old.totalextfgunta,  old.transactextacre,  old.transactextgunta,  old.transactextfgunta,  old.volumename,  old.hasgpa,  old.isaua,  old.importedpartyparentid,  
				old.salutationid,  old.isorganization,  old.organizationid,  old.applicationnumber,  old.verified,  old.issroapproved,  old.districtcode,  old.talukcode,  
				old.hoblicode,  old.villagecode,  old.tanno,  old.yearofincorp,  old.orgpoaauthsignfname,  old.orgpoaauthsignmname,  old.orgpoaauthsignlname,  old.linkpartyid,  
				old.housenumber,  old.pin,  old.propertyid,  old.propertynumber,  old.idprooftypeid,  old.isconsentwitness,  old.isprivateattendance,  old.coveringletterno,  
				old.section88file,  old.isendorseprinted,  old.thumbremarks,  old.partyidreference,  old.inserteddatetime,  old.k1k2_flag,  old.ispartyrefused,  old.islateapperance,  
				old.duplicatepartyid,  old.isduplicate,
				old.presenternamee, old.isbiometricrefused, old.iscitizennotappeared,
				old.aadharhash, old.datetimeofconsent, old.nameasperaadhar, old.digilockerid, old.isdeptaadharvalidated, old.iscitizenaadharverified,
				old.aadhaar_decline_reason, old.aadhaardeclinereason, old.idcardhash,old.isdocumentexecuted,old.isendorsementsigned,old.isthumbregistersigned,
				old.namematchpercentage,old.ispartypanverified,old.vaultid,old.transactionnumber); return old;
			
			end if;
		else return null;
	end if;   
end;
$$;


ALTER FUNCTION kavericdc.fn_partyinfo_fruits_audit() OWNER TO postgres;

--
-- Name: fn_partyschedules_fruits_audit(); Type: FUNCTION; Schema: kavericdc; Owner: postgres
--

CREATE FUNCTION kavericdc.fn_partyschedules_fruits_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
	
	if exists(
		select applicationnumber from kaveri.fruitspushkaveripayload f where applicationnumber = old.applicationnumber) then

			if tg_op = 'DELETE' then
			insert into kavericdc.partyschedules_fruits_audit
				( username ,	action ,	query , 
				partyscheduleid,partyid,scheduleid,propertyid,applicationnumber,isdelete,inserteddatetime,k1k2_flag
				)
				values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
				old.partyscheduleid,old.partyid,old.scheduleid,old.propertyid,old.applicationnumber,old.isdelete,old.inserteddatetime,old.k1k2_flag
				); return old;
			
			end if;
		else return null;
	end if;   
end;
$$;


ALTER FUNCTION kavericdc.fn_partyschedules_fruits_audit() OWNER TO postgres;

--
-- Name: fn_propertymaster_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_propertymaster_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
        insert into kavericdc.propertymaster_audit 
		(
    username ,	action ,	query ,    propertyid,     documentid ,    villagecode ,    regsrocode ,
    srocode ,    totalarea ,    unitid  ,    northboundary ,    southboundary ,    eastboundary ,    westboundary ,
    landmark ,    marketvalue ,    assessment ,    sdcalculationstring ,    stampduty ,    transferliabilities ,    consideration ,
    additionalduty ,    cessduty ,    govtduty ,    isexempted ,    exemptiondescription,    ismovableproperty  ,    sdrefund ,
    docmarketvalue ,    valid1 ,    isimdemnified ,    restriction ,    restrictiontype ,    restrictiondescription ,    enumber ,
    claimingblocknumber ,    retainingblocknumber ,    valuationreport ,    loanpurposeid ,    applicationnumber ,    verified ,
    issroapproved ,    stamparticlecode ,    stampruleid ,    regarticlecode ,    propertytypeid ,    noofscanpages ,
    movablepropertydesc ,    roadcode ,    wardid ,    pidno ,    udeptid ,    sfdastamparticlecode ,    sfdastampruleid ,
    sfdanoofscanpages ,    srostamparticlecode ,    srostampruleid ,    sronoofscanpages ,    sfdamarketvalue ,    sromarketvalue ,
    ownedarea ,    sfdanatureofdocument ,    sronatureofdocument ,    denodescription ,    estampdescription ,    adjudescription ,
    sroconsideration ,    sfdaconsideration ,    referencepropertyid ,    isbefore2004 ,    sfdastampduty ,
    srostampduty ,    sfdacessduty ,    srocessduty ,    surcharge ,    sfdasurcharge ,    srosurcharge ,
    valuationtypeid ,    inserteddatetime ,    zoneid ,    subpropertytypeid ,    k1k2_flag ,    sroroadcode ,    sfdaroadcode,
	upormutationfee, uporprcardfee, uportotalarea, uporpartarea, isuporpartextent
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
	 old.propertyid,     old.documentid ,    old.villagecode ,    old.regsrocode ,
    old.srocode ,    old.totalarea ,    old.unitid  ,    old.northboundary ,    old.southboundary ,    old.eastboundary ,    old.westboundary ,
    old.landmark ,       old.marketvalue ,    old.assessment ,    old.sdcalculationstring ,    old.stampduty ,   old.transferliabilities ,    old.consideration ,
    old.additionalduty , old.cessduty ,    old.govtduty ,    old.isexempted ,     old.exemptiondescription,  old.ismovableproperty  ,    old.sdrefund ,
    old.docmarketvalue , old.valid1 ,    old.isimdemnified , old.restriction ,    old.restrictiontype ,  old.restrictiondescription , old.enumber ,
    old.claimingblocknumber ,    old.retainingblocknumber ,  old.valuationreport ,old.loanpurposeid ,    old.applicationnumber ,  old.verified ,
    old.issroapproved ,    old.stamparticlecode ,    old.stampruleid ,    old.regarticlecode ,    old.propertytypeid ,    	old.noofscanpages ,
    old.movablepropertydesc ,    old.roadcode ,    old.wardid ,    old.pidno ,   old.udeptid ,    old.sfdastamparticlecode ,    old.sfdastampruleid ,
    old.sfdanoofscanpages ,    old.srostamparticlecode , old.srostampruleid ,    old.sronoofscanpages ,    old.sfdamarketvalue ,    old.sromarketvalue ,
    old.ownedarea ,    old.sfdanatureofdocument ,    old.sronatureofdocument ,   old.denodescription ,    old.estampdescription ,    old.adjudescription ,
    old.sroconsideration ,    old.sfdaconsideration , old.referencepropertyid ,  old.isbefore2004 ,      old.sfdastampduty ,
    old.srostampduty ,    old.sfdacessduty ,    old.srocessduty ,    old.surcharge ,    old.sfdasurcharge ,    old.srosurcharge ,
    old.valuationtypeid , old.inserteddatetime , old.zoneid ,    old.subpropertytypeid ,    old.k1k2_flag ,    old.sroroadcode ,  old.sfdaroadcode,
	old.upormutationfee, old.uporprcardfee, old.uportotalarea, old.uporpartarea, old.isuporpartextent
	); return new;	
		
	elsif tg_op = 'DELETE' then
       insert into kavericdc.propertymaster_audit 
		(
    username ,	action ,	query ,    propertyid,     documentid ,    villagecode ,    regsrocode ,
    srocode ,    totalarea ,    unitid  ,    northboundary ,    southboundary ,    eastboundary ,    westboundary ,
    landmark ,    marketvalue ,    assessment ,    sdcalculationstring ,    stampduty ,    transferliabilities ,    consideration ,
    additionalduty ,    cessduty ,    govtduty ,    isexempted ,    exemptiondescription,    ismovableproperty  ,    sdrefund ,
    docmarketvalue ,    valid1 ,    isimdemnified ,    restriction ,    restrictiontype ,    restrictiondescription ,    enumber ,
    claimingblocknumber ,    retainingblocknumber ,    valuationreport ,    loanpurposeid ,    applicationnumber ,    verified ,
    issroapproved ,    stamparticlecode ,    stampruleid ,    regarticlecode ,    propertytypeid ,    noofscanpages ,
    movablepropertydesc ,    roadcode ,    wardid ,    pidno ,    udeptid ,    sfdastamparticlecode ,    sfdastampruleid ,
    sfdanoofscanpages ,    srostamparticlecode ,    srostampruleid ,    sronoofscanpages ,    sfdamarketvalue ,    sromarketvalue ,
    ownedarea ,    sfdanatureofdocument ,    sronatureofdocument ,    denodescription ,    estampdescription ,    adjudescription ,
    sroconsideration ,    sfdaconsideration ,    referencepropertyid ,    isbefore2004 ,    sfdastampduty ,
    srostampduty ,    sfdacessduty ,    srocessduty ,    surcharge ,    sfdasurcharge ,    srosurcharge ,
    valuationtypeid ,    inserteddatetime ,    zoneid ,    subpropertytypeid ,    k1k2_flag ,    sroroadcode ,    sfdaroadcode,
	upormutationfee, uporprcardfee, uportotalarea, uporpartarea, isuporpartextent
	)
		
	 values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
	 old.propertyid,     old.documentid ,    old.villagecode ,    old.regsrocode ,
    old.srocode ,    old.totalarea ,    old.unitid  ,    old.northboundary ,    old.southboundary ,    old.eastboundary ,    old.westboundary ,
    old.landmark ,       old.marketvalue ,    old.assessment ,    old.sdcalculationstring ,    old.stampduty ,   old.transferliabilities ,    old.consideration ,
    old.additionalduty , old.cessduty ,    old.govtduty ,    old.isexempted ,     old.exemptiondescription,  old.ismovableproperty  ,    old.sdrefund ,
    old.docmarketvalue , old.valid1 ,    old.isimdemnified , old.restriction ,    old.restrictiontype ,  old.restrictiondescription , old.enumber ,
    old.claimingblocknumber ,    old.retainingblocknumber ,  old.valuationreport ,old.loanpurposeid ,    old.applicationnumber ,  old.verified ,
    old.issroapproved ,    old.stamparticlecode ,    old.stampruleid ,    old.regarticlecode ,    old.propertytypeid ,    	old.noofscanpages ,
    old.movablepropertydesc ,    old.roadcode ,    old.wardid ,    old.pidno ,   old.udeptid ,    old.sfdastamparticlecode ,    old.sfdastampruleid ,
    old.sfdanoofscanpages ,    old.srostamparticlecode , old.srostampruleid ,    old.sronoofscanpages ,    old.sfdamarketvalue ,    old.sromarketvalue ,
    old.ownedarea ,    old.sfdanatureofdocument ,    old.sronatureofdocument ,   old.denodescription ,    old.estampdescription ,    old.adjudescription ,
    old.sroconsideration ,    old.sfdaconsideration , old.referencepropertyid ,  old.isbefore2004 ,      old.sfdastampduty ,
    old.srostampduty ,    old.sfdacessduty ,    old.srocessduty ,    old.surcharge ,    old.sfdasurcharge ,    old.srosurcharge ,
    old.valuationtypeid , old.inserteddatetime , old.zoneid ,    old.subpropertytypeid ,    old.k1k2_flag ,    old.sroroadcode ,  old.sfdaroadcode,
	old.upormutationfee, old.uporprcardfee, old.uportotalarea, old.uporpartarea, old.isuporpartextent
	); return old;
    
	elsif tg_op = 'INSERT' then
	
	insert into kavericdc.propertymaster_audit 
		(
    username ,	action ,	query ,    propertyid,     documentid ,    villagecode ,    regsrocode ,
    srocode ,    totalarea ,    unitid  ,    northboundary ,    southboundary ,    eastboundary ,    westboundary ,
    landmark ,    marketvalue ,    assessment ,    sdcalculationstring ,    stampduty ,    transferliabilities ,    consideration ,
    additionalduty ,    cessduty ,    govtduty ,    isexempted ,    exemptiondescription,    ismovableproperty  ,    sdrefund ,
    docmarketvalue ,    valid1 ,    isimdemnified ,    restriction ,    restrictiontype ,    restrictiondescription ,    enumber ,
    claimingblocknumber ,    retainingblocknumber ,    valuationreport ,    loanpurposeid ,    applicationnumber ,    verified ,
    issroapproved ,    stamparticlecode ,    stampruleid ,    regarticlecode ,    propertytypeid ,    noofscanpages ,
    movablepropertydesc ,    roadcode ,    wardid ,    pidno ,    udeptid ,    sfdastamparticlecode ,    sfdastampruleid ,
    sfdanoofscanpages ,    srostamparticlecode ,    srostampruleid ,    sronoofscanpages ,    sfdamarketvalue ,    sromarketvalue ,
    ownedarea ,    sfdanatureofdocument ,    sronatureofdocument ,    denodescription ,    estampdescription ,    adjudescription ,
    sroconsideration ,    sfdaconsideration ,    referencepropertyid ,    isbefore2004 ,    sfdastampduty ,
    srostampduty ,    sfdacessduty ,    srocessduty ,    surcharge ,    sfdasurcharge ,    srosurcharge ,
    valuationtypeid ,    inserteddatetime ,    zoneid ,    subpropertytypeid ,    k1k2_flag ,    sroroadcode ,    sfdaroadcode,
	upormutationfee, uporprcardfee, uportotalarea, uporpartarea, isuporpartextent
	)
        	 values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
	 new.propertyid,     new.documentid ,    new.villagecode ,    new.regsrocode ,
    new.srocode ,    new.totalarea ,    new.unitid  ,    new.northboundary ,    new.southboundary ,    new.eastboundary ,    new.westboundary ,
    new.landmark ,       new.marketvalue ,    new.assessment ,    new.sdcalculationstring ,    new.stampduty ,   new.transferliabilities ,    new.consideration ,
    new.additionalduty , new.cessduty ,    new.govtduty ,    new.isexempted ,     new.exemptiondescription,  new.ismovableproperty  ,    new.sdrefund ,
    new.docmarketvalue , new.valid1 ,    new.isimdemnified , new.restriction ,    new.restrictiontype ,  new.restrictiondescription , new.enumber ,
    new.claimingblocknumber ,    new.retainingblocknumber ,  new.valuationreport ,new.loanpurposeid ,    new.applicationnumber ,  new.verified ,
    new.issroapproved ,    new.stamparticlecode ,    new.stampruleid ,    new.regarticlecode ,    new.propertytypeid ,    	new.noofscanpages ,
    new.movablepropertydesc ,    new.roadcode ,    new.wardid ,    new.pidno ,   new.udeptid ,    new.sfdastamparticlecode ,    new.sfdastampruleid ,
    new.sfdanoofscanpages ,    new.srostamparticlecode , new.srostampruleid ,    new.sronoofscanpages ,    new.sfdamarketvalue ,    new.sromarketvalue ,
    new.ownedarea ,    new.sfdanatureofdocument ,    new.sronatureofdocument ,   new.denodescription ,    new.estampdescription ,    new.adjudescription ,
    new.sroconsideration ,    new.sfdaconsideration , new.referencepropertyid ,  new.isbefore2004 ,      new.sfdastampduty ,
    new.srostampduty ,    new.sfdacessduty ,    new.srocessduty ,    new.surcharge ,    new.sfdasurcharge ,    new.srosurcharge ,
    new.valuationtypeid , new.inserteddatetime , new.zoneid ,    new.subpropertytypeid ,    new.k1k2_flag ,    new.sroroadcode ,  new.sfdaroadcode,
	new.upormutationfee, new.uporprcardfee, new.uportotalarea, new.uporpartarea, new.isuporpartextent
	); return new;
	
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_propertymaster_audit() OWNER TO csgadmin;

--
-- Name: fn_propertymaster_fruits_audit(); Type: FUNCTION; Schema: kavericdc; Owner: postgres
--

CREATE FUNCTION kavericdc.fn_propertymaster_fruits_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    
	if exists(
		select applicationnumber from kaveri.fruitspushkaveripayload f where applicationnumber = old.applicationnumber) then

			if tg_op = 'DELETE' then
			insert into kavericdc.propertymaster_fruits_audit 
				(
				username ,	action ,	query ,    propertyid,     documentid ,    villagecode ,    regsrocode ,
				srocode ,    totalarea ,    unitid  ,    northboundary ,    southboundary ,    eastboundary ,    westboundary ,
				landmark ,    marketvalue ,    assessment ,    sdcalculationstring ,    stampduty ,    transferliabilities ,    consideration ,
				additionalduty ,    cessduty ,    govtduty ,    isexempted ,    exemptiondescription,    ismovableproperty  ,    sdrefund ,
				docmarketvalue ,    valid1 ,    isimdemnified ,    restriction ,    restrictiontype ,    restrictiondescription ,    enumber ,
				claimingblocknumber ,    retainingblocknumber ,    valuationreport ,    loanpurposeid ,    applicationnumber ,    verified ,
				issroapproved ,    stamparticlecode ,    stampruleid ,    regarticlecode ,    propertytypeid ,    noofscanpages ,
				movablepropertydesc ,    roadcode ,    wardid ,    pidno ,    udeptid ,    sfdastamparticlecode ,    sfdastampruleid ,
				sfdanoofscanpages ,    srostamparticlecode ,    srostampruleid ,    sronoofscanpages ,    sfdamarketvalue ,    sromarketvalue ,
				ownedarea ,    sfdanatureofdocument ,    sronatureofdocument ,    denodescription ,    estampdescription ,    adjudescription ,
				sroconsideration ,    sfdaconsideration ,    referencepropertyid ,    isbefore2004 ,    sfdastampduty ,
				srostampduty ,    sfdacessduty ,    srocessduty ,    surcharge ,    sfdasurcharge ,    srosurcharge ,
				valuationtypeid ,    inserteddatetime ,    zoneid ,    subpropertytypeid ,    k1k2_flag ,    sroroadcode ,    sfdaroadcode,
				upormutationfee, uporprcardfee, uportotalarea, uporpartarea, isuporpartextent
				)
					
				 values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
				 old.propertyid,     old.documentid ,    old.villagecode ,    old.regsrocode ,
				old.srocode ,    old.totalarea ,    old.unitid  ,    old.northboundary ,    old.southboundary ,    old.eastboundary ,    old.westboundary ,
				old.landmark ,       old.marketvalue ,    old.assessment ,    old.sdcalculationstring ,    old.stampduty ,   old.transferliabilities ,    old.consideration ,
				old.additionalduty , old.cessduty ,    old.govtduty ,    old.isexempted ,     old.exemptiondescription,  old.ismovableproperty  ,    old.sdrefund ,
				old.docmarketvalue , old.valid1 ,    old.isimdemnified , old.restriction ,    old.restrictiontype ,  old.restrictiondescription , old.enumber ,
				old.claimingblocknumber ,    old.retainingblocknumber ,  old.valuationreport ,old.loanpurposeid ,    old.applicationnumber ,  old.verified ,
				old.issroapproved ,    old.stamparticlecode ,    old.stampruleid ,    old.regarticlecode ,    old.propertytypeid ,    	old.noofscanpages ,
				old.movablepropertydesc ,    old.roadcode ,    old.wardid ,    old.pidno ,   old.udeptid ,    old.sfdastamparticlecode ,    old.sfdastampruleid ,
				old.sfdanoofscanpages ,    old.srostamparticlecode , old.srostampruleid ,    old.sronoofscanpages ,    old.sfdamarketvalue ,    old.sromarketvalue ,
				old.ownedarea ,    old.sfdanatureofdocument ,    old.sronatureofdocument ,   old.denodescription ,    old.estampdescription ,    old.adjudescription ,
				old.sroconsideration ,    old.sfdaconsideration , old.referencepropertyid ,  old.isbefore2004 ,      old.sfdastampduty ,
				old.srostampduty ,    old.sfdacessduty ,    old.srocessduty ,    old.surcharge ,    old.sfdasurcharge ,    old.srosurcharge ,
				old.valuationtypeid , old.inserteddatetime , old.zoneid ,    old.subpropertytypeid ,    old.k1k2_flag ,    old.sroroadcode ,  old.sfdaroadcode,
				old.upormutationfee, old.uporprcardfee, old.uportotalarea, old.uporpartarea, old.isuporpartextent
				); return old;
			
			end if;
		else return null;
	end if;  
	
end;
$$;


ALTER FUNCTION kavericdc.fn_propertymaster_fruits_audit() OWNER TO postgres;

--
-- Name: fn_propertynumberdetails_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_propertynumberdetails_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.propertynumberdetails_audit
		( username ,	action ,	query , 
		propertyid,srocode,currentpropertytypeid,currentnumber,oldpropertytypeid,oldnumber,
		description,survey_no,surnoc,hissa_no,inserteddatetime,k1k2_flag
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.propertyid,   old.srocode,   old.currentpropertytypeid,   old.currentnumber,   old.oldpropertytypeid,   old.oldnumber,   old.description,
		old.survey_no,   old.surnoc,   old.hissa_no,   old.inserteddatetime,   old.k1k2_flag ); return new;	
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.propertynumberdetails_audit
		( username ,	action ,	query , 
		propertyid,srocode,currentpropertytypeid,currentnumber,oldpropertytypeid,oldnumber,
		description,survey_no,surnoc,hissa_no,inserteddatetime,k1k2_flag 
		)
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.propertyid,   old.srocode,   old.currentpropertytypeid,   old.currentnumber,   old.oldpropertytypeid,   old.oldnumber,   old.description,
		old.survey_no,   old.surnoc,   old.hissa_no,   old.inserteddatetime,   old.k1k2_flag); return old;
    
	elsif tg_op = 'INSERT' then
	insert into kavericdc.propertynumberdetails_audit
		( username ,	action ,	query , 
		propertyid,srocode,currentpropertytypeid,currentnumber,oldpropertytypeid,oldnumber,
		description,survey_no,surnoc,hissa_no,inserteddatetime,k1k2_flag 
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		new.propertyid,   new.srocode,   new.currentpropertytypeid,   new.currentnumber,   new.oldpropertytypeid,   new.oldnumber,   new.description,
		new.survey_no,   new.surnoc,   new.hissa_no,   new.inserteddatetime,   new.k1k2_flag); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_propertynumberdetails_audit() OWNER TO csgadmin;

--
-- Name: fn_propertyschedules_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_propertyschedules_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.propertyschedules_audit
		( username ,	action ,	query , 
		scheduleid,propertyid,srocode,partyid,scheduletype,totalarea,unitid,
		description,partyids,aileniatedauthorityid,alieniatedorder,bhoomisellerpartyids,govtrestricorder,govtrestrictionid,landcode,
		propertygroup,giftshare,giftsharedetails,easttowest,northtosouth,blockchainpropertyid,assignedblockchainpid,
		applicationnumber,verified,issroapproved,eastboundary,westboundary,northboundary,southboundary,k1k2_flag
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.scheduleid,   old.propertyid,   old.srocode,   old.partyid,   old.scheduletype,   
		old.totalarea,   old.unitid,   old.description,   old.partyids,   old.aileniatedauthorityid,   
		old.alieniatedorder,   old.bhoomisellerpartyids,   old.govtrestricorder,   old.govtrestrictionid,   old.landcode,   old.propertygroup,   
		old.giftshare,   old.giftsharedetails,   old.easttowest,   old.northtosouth,   old.blockchainpropertyid,   
		old.assignedblockchainpid,   old.applicationnumber,   old.verified,   old.issroapproved,   
		old.eastboundary,   old.westboundary,   old.northboundary,   old.southboundary,old.k1k2_flag); return new;	
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.propertyschedules_audit
		( username ,	action ,	query , 
		scheduleid,propertyid,srocode,partyid,scheduletype,totalarea,unitid,
		description,partyids,aileniatedauthorityid,alieniatedorder,bhoomisellerpartyids,govtrestricorder,govtrestrictionid,landcode,
		propertygroup,giftshare,giftsharedetails,easttowest,northtosouth,blockchainpropertyid,assignedblockchainpid,
		applicationnumber,verified,issroapproved,eastboundary,westboundary,northboundary,southboundary,k1k2_flag
		)
		values (current_user::text||' 2'||session_user::text, 'DELETED', current_query(),
		old.scheduleid,   old.propertyid,   old.srocode,   old.partyid,   old.scheduletype,   
		old.totalarea,   old.unitid,   old.description,   old.partyids,   old.aileniatedauthorityid,   
		old.alieniatedorder,   old.bhoomisellerpartyids,   old.govtrestricorder,   old.govtrestrictionid,   old.landcode,   old.propertygroup,   
		old.giftshare,   old.giftsharedetails,   old.easttowest,   old.northtosouth,   old.blockchainpropertyid,   
		old.assignedblockchainpid,   old.applicationnumber,   old.verified,   old.issroapproved,   
		old.eastboundary,   old.westboundary,   old.northboundary,   old.southboundary,old.k1k2_flag); return old;
    
	elsif tg_op = 'INSERT' then
	insert into kavericdc.propertyschedules_audit
		(  username ,	action ,	query , 
		scheduleid,propertyid,srocode,partyid,scheduletype,totalarea,unitid,
		description,partyids,aileniatedauthorityid,alieniatedorder,bhoomisellerpartyids,govtrestricorder,govtrestrictionid,landcode,
		propertygroup,giftshare,giftsharedetails,easttowest,northtosouth,blockchainpropertyid,assignedblockchainpid,
		applicationnumber,verified,issroapproved,eastboundary,westboundary,northboundary,southboundary,k1k2_flag
		)
		values (current_user::text||' 2'||session_user::text, 'INSERTED', current_query(),
		new.scheduleid,   new.propertyid,   new.srocode,   new.partyid,   new.scheduletype,   
		new.totalarea,   new.unitid,   new.description,   new.partyids,   new.aileniatedauthorityid,   
		new.alieniatedorder,   new.bhoomisellerpartyids,   new.govtrestricorder,   new.govtrestrictionid,   new.landcode,   new.propertygroup,   
		new.giftshare,   new.giftsharedetails,   new.easttowest,   new.northtosouth,   new.blockchainpropertyid,   
		new.assignedblockchainpid,   new.applicationnumber,   new.verified,   new.issroapproved,   
		new.eastboundary,   new.westboundary,   new.northboundary,   new.southboundary,new.k1k2_flag); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_propertyschedules_audit() OWNER TO csgadmin;

--
-- Name: fn_propertyschedules_fruits_audit(); Type: FUNCTION; Schema: kavericdc; Owner: postgres
--

CREATE FUNCTION kavericdc.fn_propertyschedules_fruits_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
	
	if exists(
		select applicationnumber from kaveri.fruitspushkaveripayload f where applicationnumber = old.applicationnumber) then

			if tg_op = 'DELETE' then
			insert into kavericdc.propertyschedules_fruits_audit
				( username ,	action ,	query , 
				scheduleid,propertyid,srocode,partyid,scheduletype,totalarea,unitid,description,partyids,aileniatedauthorityid,alieniatedorder,bhoomisellerpartyids,
				govtrestricorder,govtrestrictionid,landcode,propertygroup,giftshare,giftsharedetails,easttowest,northtosouth,blockchainpropertyid,assignedblockchainpid,
				applicationnumber,verified,issroapproved,eastboundary,westboundary,
				northboundary,southboundary,inserteddatetime,k1k2_flag,electriccompid,waterboardid,electriccomp,waterboard
				)
				values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
				old.scheduleid,old.propertyid,old.srocode,old.partyid,old.scheduletype,old.totalarea,old.unitid,old.description,old.partyids,old.aileniatedauthorityid,old.alieniatedorder,old.bhoomisellerpartyids,old.
				govtrestricorder,old.govtrestrictionid,old.landcode,old.propertygroup,old.giftshare,old.giftsharedetails,old.easttowest,old.northtosouth,old.blockchainpropertyid,old.assignedblockchainpid,old.
				applicationnumber,old.verified,old.issroapproved,old.eastboundary,old.westboundary,old.
				northboundary,old.southboundary,old.inserteddatetime,old.k1k2_flag,old.electriccompid,old.waterboardid,old.electriccomp,old.waterboard
				); return old;
			
			end if;
		else return null;
	end if;   
end;
$$;


ALTER FUNCTION kavericdc.fn_propertyschedules_fruits_audit() OWNER TO postgres;

--
-- Name: fn_reportmasterconfiguration_audit(); Type: FUNCTION; Schema: kavericdc; Owner: postgres
--

CREATE FUNCTION kavericdc.fn_reportmasterconfiguration_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.reportmasterconfiguration_audit
		( username ,	action ,	query , 
		id,reportid,maxyear,searchcriteriacount,feerulecode,amount,isactive,createdby,createdon,updatedby,updatedon
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.id,old.reportid,old.maxyear,old.searchcriteriacount,old.feerulecode,old.amount,old.isactive,old.createdby,old.createdon,old.updatedby,old.updatedon); return new;
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.reportmasterconfiguration_audit
		( username ,	action ,	query , 
		id,reportid,maxyear,searchcriteriacount,feerulecode,amount,isactive,createdby,createdon,updatedby,updatedon
		)
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.id,old.reportid,old.maxyear,old.searchcriteriacount,old.feerulecode,old.amount,old.isactive,old.createdby,old.createdon,old.updatedby,old.updatedon); return old;
    
	elsif tg_op = 'INSERT' then
	insert into kavericdc.reportmasterconfiguration_audit
		( username ,	action ,	query , 
		id,reportid,maxyear,searchcriteriacount,feerulecode,amount,isactive,createdby,createdon,updatedby,updatedon
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		new.id,new.reportid,new.maxyear,new.searchcriteriacount,new.feerulecode,new.amount,new.isactive,new.createdby,new.createdon,new.updatedby,new.updatedon); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_reportmasterconfiguration_audit() OWNER TO postgres;

--
-- Name: fn_sroserialmaster_audit(); Type: FUNCTION; Schema: kavericdc; Owner: csgadmin
--

CREATE FUNCTION kavericdc.fn_sroserialmaster_audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

    if tg_op = 'UPDATE' then
	insert into kavericdc.sroserialmaster_audit
		( username ,	action ,	query , 
		srocode,bookid,finyear,pendingserial,finalserial,k1k2_flag
		)
		values (current_user::text||' 2'||session_user::text, 'Updated', current_query(),
		old.srocode, old.bookid, old.finyear, old.pendingserial, old.finalserial, old.k1k2_flag); return new;	
	
	elsif tg_op = 'DELETE' then
	insert into kavericdc.sroserialmaster_audit
		( username ,	action ,	query , 
		srocode,bookid,finyear,pendingserial,finalserial,k1k2_flag
		)
		values (current_user::text||' 2'||session_user::text, 'Deleted', current_query(),
		old.srocode, old.bookid, old.finyear, old.pendingserial, old.finalserial, old.k1k2_flag); return old;
    
	elsif tg_op = 'INSERT' then
	insert into kavericdc.sroserialmaster_audit
		( username ,	action ,	query , 
		srocode,bookid,finyear,pendingserial,finalserial,k1k2_flag
		)
		values (current_user::text||' 2'||session_user::text, 'Inserted', current_query(),
		new.srocode, new.bookid, new.finyear, new.pendingserial, new.finalserial, new.k1k2_flag); return new;
   end if;
end;
$$;


ALTER FUNCTION kavericdc.fn_sroserialmaster_audit() OWNER TO csgadmin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ams_reg_epaymentamtpaiddetails_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin
--

CREATE TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    chlnrefnum character varying(23) NOT NULL,
    deptpurposeid smallint NOT NULL,
    headofaccount character varying(50) NOT NULL,
    amountpaid bigint NOT NULL,
    applicationnumber character varying(50),
    deptreferencecode character varying(18),
    totalamount bigint,
    id bigint NOT NULL,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit OWNER TO csgadmin;

--
-- Name: ams_reg_epaymentamtpaiddetails_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq OWNER TO csgadmin;

--
-- Name: ams_reg_epaymentamtpaiddetails_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq OWNED BY kavericdc.ams_reg_epaymentamtpaiddetails_audit.auditid;


--
-- Name: ams_reg_epaymentamtpaiddetails_audit_id_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq OWNER TO csgadmin;

--
-- Name: ams_reg_epaymentamtpaiddetails_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq OWNED BY kavericdc.ams_reg_epaymentamtpaiddetails_audit.id;


--
-- Name: ams_reg_epaymentbankackdetails_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin
--

CREATE TABLE kavericdc.ams_reg_epaymentbankackdetails_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    deptreferencecode character varying(18) NOT NULL,
    banktransactionnumber character varying(30) NOT NULL,
    bankname character varying(50) NOT NULL,
    paymentmode character varying(30),
    paymentstatuscode character varying(25) NOT NULL,
    transactiontimestamp timestamp without time zone NOT NULL,
    amount bigint,
    checksum character varying(100),
    transactionid bigint NOT NULL,
    bankackid bigint,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE kavericdc.ams_reg_epaymentbankackdetails_audit OWNER TO csgadmin;

--
-- Name: ams_reg_epaymentbankackdetails_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq OWNER TO csgadmin;

--
-- Name: ams_reg_epaymentbankackdetails_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq OWNED BY kavericdc.ams_reg_epaymentbankackdetails_audit.auditid;


--
-- Name: ams_reg_epaymentbankackdetails_audit_transactionid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq OWNER TO csgadmin;

--
-- Name: ams_reg_epaymentbankackdetails_audit_transactionid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq OWNED BY kavericdc.ams_reg_epaymentbankackdetails_audit.transactionid;


--
-- Name: ams_reg_epaymenttransdetails_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin
--

CREATE TABLE kavericdc.ams_reg_epaymenttransdetails_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    applicationid bigint,
    officeid smallint NOT NULL,
    remittername character varying(50) NOT NULL,
    totalamount bigint NOT NULL,
    receiptid bigint,
    chlnrefnum character varying(23),
    deptreferencecode character varying(18),
    uirnumber character varying(75),
    statuscode character varying(50),
    statusdescription character varying(100),
    transactionstatus bit(1),
    transactiondatetime timestamp without time zone,
    userid bigint,
    ipadd character varying(15),
    serviceid integer,
    paymentstatuscode character varying(25),
    ecid bigint,
    ccid bigint,
    epid bigint,
    applicationnumber character varying(50),
    treasurycode character varying(20),
    transactionid bigint NOT NULL,
    ddocode bigint,
    isdelete boolean DEFAULT false,
    lastupdateddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    documentid bigint,
    feerulecode integer,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE kavericdc.ams_reg_epaymenttransdetails_audit OWNER TO csgadmin;

--
-- Name: ams_reg_epaymenttransdetails_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq OWNER TO csgadmin;

--
-- Name: ams_reg_epaymenttransdetails_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq OWNED BY kavericdc.ams_reg_epaymenttransdetails_audit.auditid;


--
-- Name: ams_reg_epaymenttransdetails_audit_transactionid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq OWNER TO csgadmin;

--
-- Name: ams_reg_epaymenttransdetails_audit_transactionid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq OWNED BY kavericdc.ams_reg_epaymenttransdetails_audit.transactionid;


--
-- Name: applicantapplication_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin
--

CREATE TABLE kavericdc.applicantapplication_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    citizenid bigint NOT NULL,
    applicationnumber character varying(50) NOT NULL,
    srocode integer,
    regsrocode integer,
    applicationtypeid integer,
    applicationstartdate timestamp without time zone DEFAULT now(),
    applicationenddate timestamp without time zone,
    currentstatus character varying(10) NOT NULL,
    assignedto text,
    aroapplicationnumber character varying(50),
    stamparticlecode integer,
    stampruleid integer,
    deedattachpath text,
    registrationstartdate timestamp without time zone,
    registrationenddate timestamp without time zone,
    lastupdatedby text,
    regarticlecode integer,
    bookid integer,
    remarks text,
    sfdaid bigint,
    deoid bigint,
    applicationdate timestamp without time zone,
    issubmitted boolean DEFAULT false,
    isduecorrection boolean DEFAULT false,
    ispayment boolean,
    isdueschedule boolean,
    annexurepath text,
    k1k2_flag smallint DEFAULT 2,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    refuseremarks text,
    remarksk text,
    isdeleted boolean,
    ispaperless boolean,
    ispanverified boolean,
    ispanmandatory boolean
);


ALTER TABLE kavericdc.applicantapplication_audit OWNER TO csgadmin;

--
-- Name: applicantapplication_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.applicantapplication_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.applicantapplication_audit_auditid_seq OWNER TO csgadmin;

--
-- Name: applicantapplication_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.applicantapplication_audit_auditid_seq OWNED BY kavericdc.applicantapplication_audit.auditid;


--
-- Name: appointmentmaster_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin
--

CREATE TABLE kavericdc.appointmentmaster_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    appointmentid integer NOT NULL,
    appointmenttypeid integer,
    srocode integer,
    deoperator integer,
    applicationnumber character varying(50),
    appointmentdate timestamp without time zone,
    starttime time without time zone,
    endtime time without time zone,
    noofapplicants integer,
    status character varying(10),
    k1k2_flag smallint DEFAULT 2,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    reschedulefrmtool boolean DEFAULT false
);


ALTER TABLE kavericdc.appointmentmaster_audit OWNER TO csgadmin;

--
-- Name: appointmentmaster_audit_appointmentid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.appointmentmaster_audit_appointmentid_seq OWNER TO csgadmin;

--
-- Name: appointmentmaster_audit_appointmentid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq OWNED BY kavericdc.appointmentmaster_audit.appointmentid;


--
-- Name: appointmentmaster_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.appointmentmaster_audit_auditid_seq OWNER TO csgadmin;

--
-- Name: appointmentmaster_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq OWNED BY kavericdc.appointmentmaster_audit.auditid;


--
-- Name: cc_applicationdetails_audit; Type: TABLE; Schema: kavericdc; Owner: postgres
--

CREATE TABLE kavericdc.cc_applicationdetails_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    ccid bigint NOT NULL,
    ccnumber character varying(50),
    ccdate timestamp without time zone,
    userid bigint NOT NULL,
    documenttype smallint,
    kaveridrocode integer,
    kaverisrocode integer,
    documentnumber character varying(50),
    booktype smallint,
    yearofregistration character varying(50),
    pagecount integer,
    totalamount numeric(18,0),
    isappliedforsignedcopy boolean NOT NULL,
    documentstatusid smallint,
    submittedby bigint,
    submitteddatetime timestamp without time zone,
    preparedby bigint,
    prepareddatetime timestamp without time zone,
    signedby bigint,
    signeddatetime timestamp without time zone,
    appliedsignedcopy boolean,
    comparedby bigint,
    compareddatetime timestamp without time zone,
    certificatenumber character varying(50),
    accepteddatetime timestamp without time zone,
    marriagetypeid smallint,
    firmtypeid smallint,
    applicationnumber character varying(50),
    signedform22 text,
    gscno character varying,
    k1k2_flag smallint DEFAULT 2,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    isprior2003 boolean DEFAULT false NOT NULL,
    refusalremarks character varying(300),
    isrefused boolean DEFAULT false,
    finalregistrationnumber character varying(50),
    isquicksearch boolean DEFAULT false
);


ALTER TABLE kavericdc.cc_applicationdetails_audit OWNER TO postgres;

--
-- Name: cc_applicationdetails_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.cc_applicationdetails_audit_auditid_seq OWNER TO postgres;

--
-- Name: cc_applicationdetails_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq OWNED BY kavericdc.cc_applicationdetails_audit.auditid;


--
-- Name: cc_applicationdetails_audit_ccid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.cc_applicationdetails_audit_ccid_seq OWNER TO postgres;

--
-- Name: cc_applicationdetails_audit_ccid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq OWNED BY kavericdc.cc_applicationdetails_audit.ccid;


--
-- Name: departmentusers_audit; Type: TABLE; Schema: kavericdc; Owner: postgres
--

CREATE TABLE kavericdc.departmentusers_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    userid bigint,
    srocode integer NOT NULL,
    loginname text NOT NULL,
    firstname text NOT NULL,
    middlename text,
    lastname text NOT NULL,
    doj timestamp without time zone,
    designationid integer,
    emailid text,
    mobileno bigint,
    serviceflag boolean,
    serviceexpdate timestamp without time zone,
    passwd text NOT NULL,
    usertype character varying(10),
    periodfrom timestamp without time zone,
    periodto timestamp without time zone,
    bioauhreq boolean,
    digiverifyreq boolean,
    usrtype character varying(10),
    crtusr character varying(10),
    crtdate timestamp without time zone,
    joininglocation character varying(80),
    houseno_per character varying(20),
    buildingname_per character varying(80),
    streetname_per character varying(200),
    statecode_per bigint,
    villagecode_per bigint,
    districtcode_per bigint,
    pincode_per integer,
    preferaddressis_per boolean,
    houseno_curr character varying(20),
    buildingname_curr character varying(80),
    streetname_curr character varying(200),
    statecode_curr bigint,
    villagecode_curr bigint,
    districtcode_curr bigint,
    pincode_curr integer,
    emergencycontact bigint,
    uploadphoto character varying(500),
    pan character varying(10),
    status character varying(10),
    lstupdusrid bigint,
    lstupddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    officeid smallint,
    kgid text,
    createdby integer,
    employeetypeid integer,
    districtcode integer,
    groupid integer,
    isactive boolean DEFAULT true,
    isdro boolean DEFAULT false,
    surid bigint NOT NULL
);


ALTER TABLE kavericdc.departmentusers_audit OWNER TO postgres;

--
-- Name: departmentusers_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.departmentusers_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.departmentusers_audit_auditid_seq OWNER TO postgres;

--
-- Name: departmentusers_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.departmentusers_audit_auditid_seq OWNED BY kavericdc.departmentusers_audit.auditid;


--
-- Name: departmentusers_audit_surid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.departmentusers_audit_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.departmentusers_audit_surid_seq OWNER TO postgres;

--
-- Name: departmentusers_audit_surid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.departmentusers_audit_surid_seq OWNED BY kavericdc.departmentusers_audit.surid;


--
-- Name: documentmaster_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.documentmaster_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE kavericdc.documentmaster_audit_auditid_seq OWNER TO csgadmin;

SET default_tablespace = pg_default;

--
-- Name: documentmaster_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE TABLE kavericdc.documentmaster_audit (
    auditid bigint DEFAULT nextval('kavericdc.documentmaster_audit_auditid_seq'::regclass) NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    documentid bigint NOT NULL,
    srocode integer NOT NULL,
    bookid integer NOT NULL,
    stamparticlecode integer,
    regarticlecode integer NOT NULL,
    documentnumber integer,
    finalregistrationnumber character varying(50),
    presentdatetime timestamp without time zone,
    executiondatetime timestamp without time zone,
    dateofstamp timestamp without time zone,
    stamp1datetime timestamp without time zone,
    stamp2datetime timestamp without time zone,
    stamp3datetime timestamp without time zone,
    stamp4datetime timestamp without time zone,
    stamp5datetime timestamp without time zone,
    withdrawaldate timestamp without time zone,
    pagecount integer,
    index2shera character varying(250),
    isvisited boolean,
    isfiling boolean,
    ispending boolean,
    isscanned boolean,
    isrefused boolean,
    ispaymentofmoney boolean,
    isadjudicated boolean,
    iswithdrawn boolean,
    refusaldate timestamp without time zone,
    refusalreason character varying(250),
    remarksbyuser character varying(2000),
    remarksbysystem character varying(250),
    correctionreference bigint,
    olddocreference character varying(50),
    adjudicationdetails character varying(2500),
    cdnumber character varying(50),
    isxmltransferredtobhoomi boolean DEFAULT false,
    uid integer,
    pendingdocumentnumber character varying(20),
    istransmitted boolean DEFAULT false,
    isphotothumbtransmitted boolean DEFAULT false,
    inserteddatetime timestamp without time zone DEFAULT now(),
    initialtransmitted boolean,
    considerationamount numeric(23,4),
    requiredstampduty numeric(23,4),
    paidstampduty numeric(23,4),
    documentstatus character varying(5),
    applicationnumber character varying(50),
    verified boolean DEFAULT false,
    issroapproved character varying(1) DEFAULT 'E'::character varying,
    deedattachpath character varying(200),
    ispaymentdetails boolean,
    isuploaddocuments boolean,
    uploaddocdatetime timestamp without time zone,
    registrationdatetime timestamp without time zone,
    isregistrationevaluation boolean,
    uploaddocdeedpath text,
    uploaddocannexurepath text,
    docsubmitiondate timestamp without time zone,
    lstupddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    isregistrationaccepted boolean,
    isprintsummary boolean,
    isprintendorsement boolean,
    isgenerateec boolean,
    isdigitalsigned boolean,
    isregistrationcompleted boolean,
    gscno character varying(15),
    uploadsummarydocpath text,
    partypaymentdetails text,
    isscancompleted boolean,
    isundervaluation boolean DEFAULT false,
    k1k2_flag smallint DEFAULT 2,
    withdrawfilepath text,
    withdrawdocument character varying(100),
    ackdatetime timestamp without time zone,
    ackuser character varying(100),
    lateappearancepartyid bigint[],
    uploadthumbregisterpath character varying,
    isdigitallyexecuted boolean,
    issignpageappended boolean,
    isthumbregisterdocsigned boolean,
    ispendingnoteappended boolean,
    isendorsepagenumber boolean DEFAULT false,
    islegacydocscanned boolean DEFAULT false
);


ALTER TABLE kavericdc.documentmaster_audit OWNER TO csgadmin;

SET default_tablespace = '';

--
-- Name: eaasti_eswatuxmllog_audit; Type: TABLE; Schema: kavericdc; Owner: postgres
--

CREATE TABLE kavericdc.eaasti_eswatuxmllog_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    logid bigint,
    documentid bigint,
    propertyid bigint,
    pid character varying,
    xml text,
    srocode numeric,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    surid bigint NOT NULL
);


ALTER TABLE kavericdc.eaasti_eswatuxmllog_audit OWNER TO postgres;

--
-- Name: eaasti_eswatuxmllog_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq OWNER TO postgres;

--
-- Name: eaasti_eswatuxmllog_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq OWNED BY kavericdc.eaasti_eswatuxmllog_audit.auditid;


--
-- Name: eaasti_eswatuxmllog_audit_surid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.eaasti_eswatuxmllog_audit_surid_seq OWNER TO postgres;

--
-- Name: eaasti_eswatuxmllog_audit_surid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq OWNED BY kavericdc.eaasti_eswatuxmllog_audit.surid;


--
-- Name: ec_applicationdetails_audit; Type: TABLE; Schema: kavericdc; Owner: postgres
--

CREATE TABLE kavericdc.ec_applicationdetails_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    ecid bigint NOT NULL,
    ecnumber character varying(50),
    certificatenumber character varying(50),
    ecdate timestamp without time zone,
    userid bigint,
    searchfromdate date,
    searchtodate date,
    kaveridrocode smallint,
    kaverisrocode smallint,
    kaverivillagecode bigint,
    kaverihoblicode integer,
    pagecount integer,
    totalamount numeric(18,0),
    submittedby bigint,
    submitteddatetime timestamp without time zone,
    acceptedby bigint,
    acceptedon timestamp without time zone,
    documentstatusid smallint,
    preparedby bigint,
    prepareddatetime timestamp without time zone,
    signedby bigint,
    signeddatetime timestamp without time zone,
    appliedsignedcopy boolean,
    comparedby bigint,
    compareddatetime timestamp without time zone,
    eastboundary character varying(300),
    westboundary character varying(300),
    northboundary character varying(300),
    southboundary character varying(300),
    easttowest character varying(300),
    northtosouth character varying(300),
    remarktoreprepareec character varying(200),
    area numeric(18,0),
    propertydescription character varying(10485760),
    measurementunitid smallint,
    hectare numeric(18,0),
    acre numeric(18,0),
    gunta numeric(18,0),
    cents numeric(18,0),
    partyname character varying(200),
    isnamesearch boolean,
    ispropertysearch boolean,
    isdocviewable boolean,
    applicationnumber character varying(50),
    easttowestmeasurement character varying(18),
    northtosouthmeasurement character varying(18),
    propertytypeid integer,
    signedform22 text,
    gscno character varying,
    k1k2_flag smallint DEFAULT 2,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    reason character varying(150),
    isappliedbydept boolean,
    isbefore2004 boolean DEFAULT false,
    refusalremarks character varying(300),
    isrefused boolean DEFAULT false
);


ALTER TABLE kavericdc.ec_applicationdetails_audit OWNER TO postgres;

--
-- Name: ec_applicationdetails_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.ec_applicationdetails_audit_auditid_seq OWNER TO postgres;

--
-- Name: ec_applicationdetails_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq OWNED BY kavericdc.ec_applicationdetails_audit.auditid;


--
-- Name: feesrequired_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.feesrequired_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE kavericdc.feesrequired_audit_auditid_seq OWNER TO csgadmin;

SET default_tablespace = pg_default;

--
-- Name: feesrequired_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE TABLE kavericdc.feesrequired_audit (
    auditid bigint DEFAULT nextval('kavericdc.feesrequired_audit_auditid_seq'::regclass) NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    documentid bigint,
    feerulecode integer NOT NULL,
    isexempted boolean,
    exemptdescription character varying(200),
    isactive boolean,
    feecalculationstring character varying(500),
    srocode integer,
    isonline boolean,
    amountrequired numeric(23,4),
    applicationnumber character varying(50),
    propertyid bigint,
    lastupdateddate timestamp without time zone,
    exemtype character varying(50),
    exemamount integer,
    exemdocpath character varying(500),
    denodocpath character varying(500),
    sfdaamountrequired numeric(23,4),
    sroamountrequired numeric(23,4),
    amountpaid numeric(23,4),
    valuatiotypeid smallint,
    sfdastamprule integer,
    srostamprule integer,
    regexemtype character varying(50),
    regexemamount integer,
    paymentstatus character varying(15),
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    receiptid bigint,
    undervaluationamount numeric(23,4)
);


ALTER TABLE kavericdc.feesrequired_audit OWNER TO csgadmin;

--
-- Name: mdm_audit_table_audit_id_seq1; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE kavericdc.mdm_audit_table_audit_id_seq1 OWNER TO csgadmin;

SET default_tablespace = '';

--
-- Name: mdm_audit_table; Type: TABLE; Schema: kavericdc; Owner: csgadmin
--

CREATE TABLE kavericdc.mdm_audit_table (
    audit_id integer DEFAULT nextval('kavericdc.mdm_audit_table_audit_id_seq1'::regclass) NOT NULL,
    table_name character varying(200) NOT NULL,
    user_name character varying(100) NOT NULL,
    action_timestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    action character varying(8) NOT NULL,
    old_values kaveri.hstore,
    new_values kaveri.hstore,
    updated_cols text[],
    query text
);


ALTER TABLE kavericdc.mdm_audit_table OWNER TO csgadmin;

--
-- Name: minutebook_data_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin
--

CREATE TABLE kavericdc.minutebook_data_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    docid bigint,
    applicationnumber character varying(50),
    remarks character varying(500),
    issystem boolean,
    minutedate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    srocode integer,
    reasonid integer,
    remark_comment text,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    private_remark text,
    dr_order_number character varying,
    dr_order_filepath character varying,
    ispendingdocument boolean DEFAULT false,
    pendingregistrationnumber text,
    isbefore2003 boolean
);


ALTER TABLE kavericdc.minutebook_data_audit OWNER TO csgadmin;

--
-- Name: minutebook_data_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.minutebook_data_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.minutebook_data_audit_auditid_seq OWNER TO csgadmin;

--
-- Name: minutebook_data_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.minutebook_data_audit_auditid_seq OWNED BY kavericdc.minutebook_data_audit.auditid;


--
-- Name: partyinfo_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.partyinfo_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE kavericdc.partyinfo_audit_auditid_seq OWNER TO csgadmin;

SET default_tablespace = pg_default;

--
-- Name: partyinfo_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE TABLE kavericdc.partyinfo_audit (
    auditid bigint DEFAULT nextval('kavericdc.partyinfo_audit_auditid_seq'::regclass) NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    partyid bigint NOT NULL,
    srocode integer NOT NULL,
    documentid bigint NOT NULL,
    partytypeid integer NOT NULL,
    firstname character varying(300),
    middlename character varying(300),
    lastname character varying(350),
    address character varying(300) NOT NULL,
    age character varying(3),
    sex smallint,
    isexecutor boolean NOT NULL,
    ispresenter boolean NOT NULL,
    admissiondate timestamp without time zone,
    aliasname character varying(150),
    correctedname character varying(150),
    relationship character varying(50),
    relativename character varying(200),
    epic character varying(50),
    pan character varying(50),
    phonenumber character varying(15),
    availableextacre integer,
    availableextgunta integer,
    availableextfgunta numeric(7,5),
    bincom character varying(50),
    category character varying(120),
    dateofdeath timestamp without time zone,
    fingerid integer,
    fingerverificationstatusid smallint,
    ispartofrtc boolean,
    landcode bigint,
    mainownerno bigint,
    ownerno bigint,
    partypoa character varying(350),
    photopath character varying(256),
    poaadmission bigint,
    poapresentation bigint,
    primaryseller boolean,
    profession character varying(100),
    restriction character varying(1),
    restrictiondescription character varying(120),
    restrictiontype character varying(2),
    section88exemption boolean,
    thumbmatchfailedreasonid integer,
    thumbminutiae bytea,
    thumbpath character varying(256),
    totalextacre integer,
    totalextgunta integer,
    totalextfgunta numeric(7,5),
    transactextacre integer,
    transactextgunta integer,
    transactextfgunta numeric(7,5),
    volumename character varying(50),
    hasgpa boolean,
    isaua boolean,
    importedpartyparentid bigint,
    salutationid smallint,
    isorganization boolean DEFAULT false,
    organizationid integer,
    applicationnumber character varying(50),
    verified boolean DEFAULT false,
    issroapproved character varying(1) DEFAULT 'E'::character varying,
    districtcode integer,
    talukcode integer,
    hoblicode integer,
    villagecode bigint,
    tanno character varying(50),
    yearofincorp integer,
    orgpoaauthsignfname text,
    orgpoaauthsignmname text,
    orgpoaauthsignlname text,
    linkpartyid bigint,
    housenumber text,
    pin integer,
    propertyid bigint,
    propertynumber character varying,
    idprooftypeid smallint,
    isconsentwitness boolean,
    isprivateattendance boolean DEFAULT false,
    coveringletterno character(100),
    section88file character(500),
    isendorseprinted boolean DEFAULT false,
    thumbremarks character varying(200),
    partyidreference bigint,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    ispartyrefused boolean DEFAULT false,
    islateapperance boolean DEFAULT false,
    duplicatepartyid bigint,
    isduplicate boolean,
    presenternamee character varying(100),
    isbiometricrefused boolean DEFAULT false NOT NULL,
    iscitizennotappeared boolean DEFAULT false,
    aadharhash character varying(500),
    datetimeofconsent character varying,
    nameasperaadhar character varying(500),
    digilockerid character varying,
    isdeptaadharvalidated boolean DEFAULT false NOT NULL,
    iscitizenaadharverified boolean DEFAULT false NOT NULL,
    aadhaar_decline_reason character varying,
    aadhaardeclinereason character varying,
    idcardhash text,
    isdocumentexecuted boolean,
    isendorsementsigned boolean,
    isthumbregistersigned boolean,
    namematchpercentage integer,
    ispartypanverified boolean,
    vaultid character varying,
    transactionnumber character varying
);


ALTER TABLE kavericdc.partyinfo_audit OWNER TO csgadmin;

SET default_tablespace = '';

--
-- Name: partyinfo_fruits_audit; Type: TABLE; Schema: kavericdc; Owner: postgres
--

CREATE TABLE kavericdc.partyinfo_fruits_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    partyid bigint NOT NULL,
    srocode integer NOT NULL,
    documentid bigint NOT NULL,
    partytypeid integer NOT NULL,
    firstname character varying(300),
    middlename character varying(300),
    lastname character varying(350),
    address character varying(300) NOT NULL,
    age character varying(3),
    sex smallint,
    isexecutor boolean NOT NULL,
    ispresenter boolean NOT NULL,
    admissiondate timestamp without time zone,
    aliasname character varying(150),
    correctedname character varying(150),
    relationship character varying(50),
    relativename character varying(200),
    epic character varying(50),
    pan character varying(50),
    phonenumber character varying(15),
    availableextacre integer,
    availableextgunta integer,
    availableextfgunta numeric(7,5),
    bincom character varying(50),
    category character varying(120),
    dateofdeath timestamp without time zone,
    fingerid integer,
    fingerverificationstatusid smallint,
    ispartofrtc boolean,
    landcode bigint,
    mainownerno bigint,
    ownerno bigint,
    partypoa character varying(350),
    photopath character varying(256),
    poaadmission bigint,
    poapresentation bigint,
    primaryseller boolean,
    profession character varying(100),
    restriction character varying(1),
    restrictiondescription character varying(120),
    restrictiontype character varying(2),
    section88exemption boolean,
    thumbmatchfailedreasonid integer,
    thumbminutiae bytea,
    thumbpath character varying(256),
    totalextacre integer,
    totalextgunta integer,
    totalextfgunta numeric(7,5),
    transactextacre integer,
    transactextgunta integer,
    transactextfgunta numeric(7,5),
    volumename character varying(50),
    hasgpa boolean,
    isaua boolean,
    importedpartyparentid bigint,
    salutationid smallint,
    isorganization boolean DEFAULT false,
    organizationid integer,
    applicationnumber character varying(50),
    verified boolean DEFAULT false,
    issroapproved character varying(1) DEFAULT 'E'::character varying,
    districtcode integer,
    talukcode integer,
    hoblicode integer,
    villagecode bigint,
    tanno character varying(50),
    yearofincorp integer,
    orgpoaauthsignfname text,
    orgpoaauthsignmname text,
    orgpoaauthsignlname text,
    linkpartyid bigint,
    housenumber text,
    pin integer,
    propertyid bigint,
    propertynumber character varying,
    idprooftypeid smallint,
    isconsentwitness boolean,
    isprivateattendance boolean DEFAULT false,
    coveringletterno character(100),
    section88file character(500),
    isendorseprinted boolean DEFAULT false,
    thumbremarks character varying(200),
    partyidreference bigint,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    ispartyrefused boolean DEFAULT false,
    islateapperance boolean DEFAULT false,
    duplicatepartyid bigint,
    isduplicate boolean,
    presenternamee character varying(100),
    isbiometricrefused boolean DEFAULT false NOT NULL,
    iscitizennotappeared boolean DEFAULT false,
    aadharhash character varying(500),
    datetimeofconsent character varying,
    nameasperaadhar character varying(500),
    digilockerid character varying,
    isdeptaadharvalidated boolean DEFAULT false NOT NULL,
    iscitizenaadharverified boolean DEFAULT false NOT NULL,
    aadhaar_decline_reason character varying,
    aadhaardeclinereason character varying,
    idcardhash text,
    isdocumentexecuted boolean DEFAULT false,
    isendorsementsigned boolean DEFAULT false,
    isthumbregistersigned boolean DEFAULT false,
    namematchpercentage integer,
    ispartypanverified boolean DEFAULT false,
    vaultid character varying,
    transactionnumber character varying
);


ALTER TABLE kavericdc.partyinfo_fruits_audit OWNER TO postgres;

--
-- Name: partyinfo_fruits_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.partyinfo_fruits_audit_auditid_seq OWNER TO postgres;

--
-- Name: partyinfo_fruits_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq OWNED BY kavericdc.partyinfo_fruits_audit.auditid;


--
-- Name: partyschedules_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin
--

CREATE TABLE kavericdc.partyschedules_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    partyscheduleid bigint NOT NULL,
    partyid bigint NOT NULL,
    scheduleid bigint NOT NULL,
    propertyid bigint NOT NULL,
    applicationnumber character varying(50),
    isdelete boolean DEFAULT false,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE kavericdc.partyschedules_audit OWNER TO csgadmin;

--
-- Name: partyschedules_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.partyschedules_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.partyschedules_audit_auditid_seq OWNER TO csgadmin;

--
-- Name: partyschedules_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.partyschedules_audit_auditid_seq OWNED BY kavericdc.partyschedules_audit.auditid;


--
-- Name: partyschedules_audit_partyscheduleid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.partyschedules_audit_partyscheduleid_seq OWNER TO csgadmin;

--
-- Name: partyschedules_audit_partyscheduleid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq OWNED BY kavericdc.partyschedules_audit.partyscheduleid;


--
-- Name: partyschedules_fruits_audit; Type: TABLE; Schema: kavericdc; Owner: postgres
--

CREATE TABLE kavericdc.partyschedules_fruits_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    partyscheduleid bigint NOT NULL,
    partyid bigint NOT NULL,
    scheduleid bigint NOT NULL,
    propertyid bigint NOT NULL,
    applicationnumber character varying(50),
    isdelete boolean DEFAULT false,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE kavericdc.partyschedules_fruits_audit OWNER TO postgres;

--
-- Name: partyschedules_fruits_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.partyschedules_fruits_audit_auditid_seq OWNER TO postgres;

--
-- Name: partyschedules_fruits_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq OWNED BY kavericdc.partyschedules_fruits_audit.auditid;


--
-- Name: partyschedules_fruits_audit_partyscheduleid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq OWNER TO postgres;

--
-- Name: partyschedules_fruits_audit_partyscheduleid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq OWNED BY kavericdc.partyschedules_fruits_audit.partyscheduleid;


--
-- Name: propertymaster_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.propertymaster_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE kavericdc.propertymaster_audit_auditid_seq OWNER TO csgadmin;

SET default_tablespace = pg_default;

--
-- Name: propertymaster_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE TABLE kavericdc.propertymaster_audit (
    auditid bigint DEFAULT nextval('kavericdc.propertymaster_audit_auditid_seq'::regclass) NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    propertyid bigint NOT NULL,
    documentid bigint NOT NULL,
    villagecode bigint,
    regsrocode integer NOT NULL,
    srocode integer NOT NULL,
    totalarea numeric(18,4) NOT NULL,
    unitid integer NOT NULL,
    northboundary character varying(500),
    southboundary character varying(500),
    eastboundary character varying(500),
    westboundary character varying(500),
    landmark character varying(5000),
    marketvalue numeric,
    assessment character varying(2000),
    sdcalculationstring character varying(500),
    stampduty numeric,
    transferliabilities smallint,
    consideration numeric,
    additionalduty numeric,
    cessduty numeric,
    govtduty numeric,
    isexempted boolean,
    exemptiondescription character varying(2000),
    ismovableproperty boolean NOT NULL,
    sdrefund numeric,
    docmarketvalue numeric,
    valid1 bigint,
    isimdemnified boolean,
    restriction character varying(1),
    restrictiontype character varying(2),
    restrictiondescription character varying(120),
    enumber character varying(20),
    claimingblocknumber character varying(1),
    retainingblocknumber character varying(1),
    valuationreport character varying(4000),
    loanpurposeid smallint,
    applicationnumber character varying(50),
    verified boolean DEFAULT false,
    issroapproved character varying(1),
    stamparticlecode integer,
    stampruleid integer,
    regarticlecode integer,
    propertytypeid integer,
    noofscanpages integer,
    movablepropertydesc text,
    roadcode bigint,
    wardid integer,
    pidno bigint,
    udeptid integer,
    sfdastamparticlecode integer,
    sfdastampruleid integer,
    sfdanoofscanpages integer,
    srostamparticlecode integer,
    srostampruleid integer,
    sronoofscanpages integer,
    sfdamarketvalue bigint,
    sromarketvalue bigint,
    ownedarea numeric(18,4),
    sfdanatureofdocument integer,
    sronatureofdocument integer,
    denodescription character varying,
    estampdescription character varying,
    adjudescription character varying,
    sroconsideration numeric,
    sfdaconsideration numeric,
    referencepropertyid bigint,
    isbefore2004 boolean,
    sfdastampduty numeric,
    srostampduty numeric,
    sfdacessduty numeric,
    srocessduty numeric,
    surcharge numeric,
    sfdasurcharge numeric,
    srosurcharge numeric,
    valuationtypeid smallint,
    inserteddatetime timestamp without time zone,
    zoneid integer,
    subpropertytypeid integer,
    k1k2_flag smallint,
    sroroadcode bigint,
    sfdaroadcode bigint,
    upormutationfee numeric DEFAULT 0,
    uporprcardfee numeric DEFAULT 0,
    uportotalarea numeric(20,6),
    uporpartarea numeric(20,6),
    isuporpartextent boolean DEFAULT false
);


ALTER TABLE kavericdc.propertymaster_audit OWNER TO csgadmin;

SET default_tablespace = '';

--
-- Name: propertymaster_fruits_audit; Type: TABLE; Schema: kavericdc; Owner: postgres
--

CREATE TABLE kavericdc.propertymaster_fruits_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    propertyid bigint NOT NULL,
    documentid bigint NOT NULL,
    villagecode bigint,
    regsrocode integer NOT NULL,
    srocode integer NOT NULL,
    totalarea numeric(20,6) NOT NULL,
    unitid integer NOT NULL,
    northboundary character varying(500),
    southboundary character varying(500),
    eastboundary character varying(500),
    westboundary character varying(500),
    landmark character varying(5000),
    marketvalue numeric,
    assessment character varying(2000),
    sdcalculationstring character varying(500),
    stampduty numeric,
    transferliabilities smallint,
    consideration numeric,
    additionalduty numeric,
    cessduty numeric,
    govtduty numeric,
    isexempted boolean,
    exemptiondescription character varying(2000),
    ismovableproperty boolean NOT NULL,
    sdrefund numeric,
    docmarketvalue numeric,
    valid1 bigint,
    isimdemnified boolean,
    restriction character varying(1),
    restrictiontype character varying(2),
    restrictiondescription character varying(120),
    enumber character varying(20),
    claimingblocknumber character varying(1),
    retainingblocknumber character varying(1),
    valuationreport character varying(4000),
    loanpurposeid smallint,
    applicationnumber character varying(50),
    verified boolean DEFAULT false,
    issroapproved character varying(1) DEFAULT 'E'::character varying,
    stamparticlecode integer,
    stampruleid integer,
    regarticlecode integer,
    propertytypeid integer,
    noofscanpages integer,
    movablepropertydesc text,
    roadcode bigint,
    wardid integer,
    pidno bigint,
    udeptid integer,
    sfdastamparticlecode integer,
    sfdastampruleid integer,
    sfdanoofscanpages integer,
    srostamparticlecode integer,
    srostampruleid integer,
    sronoofscanpages integer,
    sfdamarketvalue bigint,
    sromarketvalue bigint,
    ownedarea numeric(20,6),
    sfdanatureofdocument integer,
    sronatureofdocument integer,
    denodescription character varying,
    estampdescription character varying,
    adjudescription character varying,
    sroconsideration numeric,
    sfdaconsideration numeric,
    referencepropertyid bigint,
    isbefore2004 boolean,
    sfdastampduty numeric,
    srostampduty numeric,
    sfdacessduty numeric,
    srocessduty numeric,
    surcharge numeric,
    sfdasurcharge numeric,
    srosurcharge numeric,
    valuationtypeid smallint,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    zoneid integer,
    subpropertytypeid integer,
    k1k2_flag smallint DEFAULT 2,
    sroroadcode bigint,
    sfdaroadcode bigint,
    upormutationfee numeric DEFAULT 0,
    uporprcardfee numeric DEFAULT 0,
    uportotalarea numeric(20,6),
    uporpartarea numeric(20,6),
    isuporpartextent boolean DEFAULT false
);


ALTER TABLE kavericdc.propertymaster_fruits_audit OWNER TO postgres;

--
-- Name: propertymaster_fruits_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.propertymaster_fruits_audit_auditid_seq OWNER TO postgres;

--
-- Name: propertymaster_fruits_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq OWNED BY kavericdc.propertymaster_fruits_audit.auditid;


--
-- Name: propertynumberdetails_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE kavericdc.propertynumberdetails_audit_auditid_seq OWNER TO csgadmin;

SET default_tablespace = pg_default;

--
-- Name: propertynumberdetails_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE TABLE kavericdc.propertynumberdetails_audit (
    auditid bigint DEFAULT nextval('kavericdc.propertynumberdetails_audit_auditid_seq'::regclass) NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    propertyid bigint NOT NULL,
    srocode integer NOT NULL,
    currentpropertytypeid integer NOT NULL,
    currentnumber character varying(100) NOT NULL,
    oldpropertytypeid integer,
    oldnumber character varying(75),
    description character varying(1000),
    survey_no integer,
    surnoc character varying(20),
    hissa_no character varying(30),
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE kavericdc.propertynumberdetails_audit OWNER TO csgadmin;

SET default_tablespace = '';

--
-- Name: propertyschedules_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin
--

CREATE TABLE kavericdc.propertyschedules_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    scheduleid bigint,
    propertyid bigint NOT NULL,
    srocode integer NOT NULL,
    partyid bigint,
    scheduletype character varying(6),
    totalarea numeric(18,6) NOT NULL,
    unitid integer NOT NULL,
    description character varying(5000) NOT NULL,
    partyids character varying(2000),
    aileniatedauthorityid boolean,
    alieniatedorder character varying(200),
    bhoomisellerpartyids character varying(2000),
    govtrestricorder character varying(200),
    govtrestrictionid boolean,
    landcode bigint,
    propertygroup smallint,
    giftshare numeric(18,2),
    giftsharedetails character varying(200),
    easttowest character varying(500),
    northtosouth character varying(500),
    blockchainpropertyid character varying(200),
    assignedblockchainpid character varying(200),
    applicationnumber character varying(50),
    verified boolean DEFAULT false,
    issroapproved character varying(1) DEFAULT 'E'::character varying,
    eastboundary character varying(500),
    westboundary character varying(500),
    northboundary character varying(500),
    southboundary character varying(500),
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE kavericdc.propertyschedules_audit OWNER TO csgadmin;

--
-- Name: propertyschedules_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.propertyschedules_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.propertyschedules_audit_auditid_seq OWNER TO csgadmin;

--
-- Name: propertyschedules_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: csgadmin
--

ALTER SEQUENCE kavericdc.propertyschedules_audit_auditid_seq OWNED BY kavericdc.propertyschedules_audit.auditid;


--
-- Name: propertyschedules_fruits_audit; Type: TABLE; Schema: kavericdc; Owner: postgres
--

CREATE TABLE kavericdc.propertyschedules_fruits_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    scheduleid bigint NOT NULL,
    propertyid bigint NOT NULL,
    srocode integer NOT NULL,
    partyid bigint,
    scheduletype character varying(6),
    totalarea numeric(20,6) NOT NULL,
    unitid integer NOT NULL,
    description character varying(15000) NOT NULL,
    partyids character varying(2000),
    aileniatedauthorityid boolean,
    alieniatedorder character varying(200),
    bhoomisellerpartyids character varying(2000),
    govtrestricorder character varying(200),
    govtrestrictionid boolean,
    landcode bigint,
    propertygroup smallint,
    giftshare numeric(18,2),
    giftsharedetails character varying(200),
    easttowest character varying(500),
    northtosouth character varying(500),
    blockchainpropertyid character varying(200),
    assignedblockchainpid character varying(200),
    applicationnumber character varying(50),
    verified boolean DEFAULT false,
    issroapproved character varying(1) DEFAULT 'E'::character varying,
    eastboundary character varying(500),
    westboundary character varying(500),
    northboundary character varying(500),
    southboundary character varying(500),
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    electriccompid character varying(100),
    waterboardid character varying(100),
    electriccomp integer,
    waterboard integer
);


ALTER TABLE kavericdc.propertyschedules_fruits_audit OWNER TO postgres;

--
-- Name: propertyschedules_fruits_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.propertyschedules_fruits_audit_auditid_seq OWNER TO postgres;

--
-- Name: propertyschedules_fruits_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq OWNED BY kavericdc.propertyschedules_fruits_audit.auditid;


--
-- Name: reportmasterconfiguration_audit; Type: TABLE; Schema: kavericdc; Owner: postgres
--

CREATE TABLE kavericdc.reportmasterconfiguration_audit (
    auditid bigint NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    id bigint NOT NULL,
    reportid integer NOT NULL,
    maxyear integer NOT NULL,
    searchcriteriacount integer NOT NULL,
    feerulecode integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    isactive boolean DEFAULT true,
    createdby bigint,
    createdon timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updatedby bigint,
    updatedon timestamp without time zone,
    surid bigint NOT NULL
);


ALTER TABLE kavericdc.reportmasterconfiguration_audit OWNER TO postgres;

--
-- Name: reportmasterconfiguration_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.reportmasterconfiguration_audit_auditid_seq OWNER TO postgres;

--
-- Name: reportmasterconfiguration_audit_auditid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq OWNED BY kavericdc.reportmasterconfiguration_audit.auditid;


--
-- Name: reportmasterconfiguration_audit_surid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: postgres
--

CREATE SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kavericdc.reportmasterconfiguration_audit_surid_seq OWNER TO postgres;

--
-- Name: reportmasterconfiguration_audit_surid_seq; Type: SEQUENCE OWNED BY; Schema: kavericdc; Owner: postgres
--

ALTER SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq OWNED BY kavericdc.reportmasterconfiguration_audit.surid;


--
-- Name: sroserialmaster_audit_auditid_seq; Type: SEQUENCE; Schema: kavericdc; Owner: csgadmin
--

CREATE SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE kavericdc.sroserialmaster_audit_auditid_seq OWNER TO csgadmin;

SET default_tablespace = pg_default;

--
-- Name: sroserialmaster_audit; Type: TABLE; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE TABLE kavericdc.sroserialmaster_audit (
    auditid bigint DEFAULT nextval('kavericdc.sroserialmaster_audit_auditid_seq'::regclass) NOT NULL,
    logdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username character varying(100),
    action character varying(50),
    query text,
    srocode integer NOT NULL,
    bookid integer NOT NULL,
    finyear character varying(20) NOT NULL,
    pendingserial bigint DEFAULT 0,
    finalserial bigint DEFAULT 0,
    k1k2_flag smallint DEFAULT 2,
    insertdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE kavericdc.sroserialmaster_audit OWNER TO csgadmin;

--
-- Name: ams_reg_epaymentamtpaiddetails_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.ams_reg_epaymentamtpaiddetails_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq'::regclass);


--
-- Name: ams_reg_epaymentamtpaiddetails_audit id; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.ams_reg_epaymentamtpaiddetails_audit ALTER COLUMN id SET DEFAULT nextval('kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq'::regclass);


--
-- Name: ams_reg_epaymentbankackdetails_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.ams_reg_epaymentbankackdetails_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq'::regclass);


--
-- Name: ams_reg_epaymentbankackdetails_audit transactionid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.ams_reg_epaymentbankackdetails_audit ALTER COLUMN transactionid SET DEFAULT nextval('kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq'::regclass);


--
-- Name: ams_reg_epaymenttransdetails_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.ams_reg_epaymenttransdetails_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq'::regclass);


--
-- Name: ams_reg_epaymenttransdetails_audit transactionid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.ams_reg_epaymenttransdetails_audit ALTER COLUMN transactionid SET DEFAULT nextval('kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq'::regclass);


--
-- Name: applicantapplication_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.applicantapplication_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.applicantapplication_audit_auditid_seq'::regclass);


--
-- Name: appointmentmaster_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.appointmentmaster_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.appointmentmaster_audit_auditid_seq'::regclass);


--
-- Name: appointmentmaster_audit appointmentid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.appointmentmaster_audit ALTER COLUMN appointmentid SET DEFAULT nextval('kavericdc.appointmentmaster_audit_appointmentid_seq'::regclass);


--
-- Name: cc_applicationdetails_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.cc_applicationdetails_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.cc_applicationdetails_audit_auditid_seq'::regclass);


--
-- Name: cc_applicationdetails_audit ccid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.cc_applicationdetails_audit ALTER COLUMN ccid SET DEFAULT nextval('kavericdc.cc_applicationdetails_audit_ccid_seq'::regclass);


--
-- Name: departmentusers_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.departmentusers_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.departmentusers_audit_auditid_seq'::regclass);


--
-- Name: departmentusers_audit surid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.departmentusers_audit ALTER COLUMN surid SET DEFAULT nextval('kavericdc.departmentusers_audit_surid_seq'::regclass);


--
-- Name: eaasti_eswatuxmllog_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.eaasti_eswatuxmllog_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.eaasti_eswatuxmllog_audit_auditid_seq'::regclass);


--
-- Name: eaasti_eswatuxmllog_audit surid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.eaasti_eswatuxmllog_audit ALTER COLUMN surid SET DEFAULT nextval('kavericdc.eaasti_eswatuxmllog_audit_surid_seq'::regclass);


--
-- Name: ec_applicationdetails_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.ec_applicationdetails_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.ec_applicationdetails_audit_auditid_seq'::regclass);


--
-- Name: minutebook_data_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.minutebook_data_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.minutebook_data_audit_auditid_seq'::regclass);


--
-- Name: partyinfo_fruits_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.partyinfo_fruits_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.partyinfo_fruits_audit_auditid_seq'::regclass);


--
-- Name: partyschedules_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.partyschedules_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.partyschedules_audit_auditid_seq'::regclass);


--
-- Name: partyschedules_audit partyscheduleid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.partyschedules_audit ALTER COLUMN partyscheduleid SET DEFAULT nextval('kavericdc.partyschedules_audit_partyscheduleid_seq'::regclass);


--
-- Name: partyschedules_fruits_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.partyschedules_fruits_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.partyschedules_fruits_audit_auditid_seq'::regclass);


--
-- Name: partyschedules_fruits_audit partyscheduleid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.partyschedules_fruits_audit ALTER COLUMN partyscheduleid SET DEFAULT nextval('kavericdc.partyschedules_fruits_audit_partyscheduleid_seq'::regclass);


--
-- Name: propertymaster_fruits_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.propertymaster_fruits_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.propertymaster_fruits_audit_auditid_seq'::regclass);


--
-- Name: propertyschedules_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.propertyschedules_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.propertyschedules_audit_auditid_seq'::regclass);


--
-- Name: propertyschedules_fruits_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.propertyschedules_fruits_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.propertyschedules_fruits_audit_auditid_seq'::regclass);


--
-- Name: reportmasterconfiguration_audit auditid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.reportmasterconfiguration_audit ALTER COLUMN auditid SET DEFAULT nextval('kavericdc.reportmasterconfiguration_audit_auditid_seq'::regclass);


--
-- Name: reportmasterconfiguration_audit surid; Type: DEFAULT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.reportmasterconfiguration_audit ALTER COLUMN surid SET DEFAULT nextval('kavericdc.reportmasterconfiguration_audit_surid_seq'::regclass);


SET default_tablespace = '';

--
-- Name: appointmentmaster_audit appointmentmaster_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.appointmentmaster_audit
    ADD CONSTRAINT appointmentmaster_audit_pkey PRIMARY KEY (auditid);


--
-- Name: cc_applicationdetails_audit cc_applicationdetails_audit_pkey1; Type: CONSTRAINT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.cc_applicationdetails_audit
    ADD CONSTRAINT cc_applicationdetails_audit_pkey1 PRIMARY KEY (auditid);


--
-- Name: departmentusers_audit departmentusers_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.departmentusers_audit
    ADD CONSTRAINT departmentusers_audit_pkey PRIMARY KEY (surid);


--
-- Name: documentmaster_audit documentmaster_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.documentmaster_audit
    ADD CONSTRAINT documentmaster_audit_pkey PRIMARY KEY (auditid);


--
-- Name: eaasti_eswatuxmllog_audit eaasti_eswatuxmllog_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.eaasti_eswatuxmllog_audit
    ADD CONSTRAINT eaasti_eswatuxmllog_audit_pkey PRIMARY KEY (surid);


--
-- Name: ec_applicationdetails_audit ec_app_audit_pkey1; Type: CONSTRAINT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.ec_applicationdetails_audit
    ADD CONSTRAINT ec_app_audit_pkey1 PRIMARY KEY (auditid);


--
-- Name: feesrequired_audit feesrequired_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.feesrequired_audit
    ADD CONSTRAINT feesrequired_audit_pkey PRIMARY KEY (auditid);


--
-- Name: mdm_audit_table mdm_audit_table_pkey1; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.mdm_audit_table
    ADD CONSTRAINT mdm_audit_table_pkey1 PRIMARY KEY (audit_id);


--
-- Name: partyinfo_audit partyinfo_audit_pkey1; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.partyinfo_audit
    ADD CONSTRAINT partyinfo_audit_pkey1 PRIMARY KEY (auditid);


--
-- Name: partyinfo_fruits_audit partyinfo_fruits_audit_pkey1; Type: CONSTRAINT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.partyinfo_fruits_audit
    ADD CONSTRAINT partyinfo_fruits_audit_pkey1 PRIMARY KEY (auditid);


--
-- Name: partyschedules_audit partyschedules_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.partyschedules_audit
    ADD CONSTRAINT partyschedules_pkey PRIMARY KEY (scheduleid, propertyid, partyid);


--
-- Name: applicantapplication_audit pk_applicationaudit_auditid; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.applicantapplication_audit
    ADD CONSTRAINT pk_applicationaudit_auditid PRIMARY KEY (auditid);


--
-- Name: ams_reg_epaymentamtpaiddetails_audit pk_id_ams_reg_epaymentamtpaiddetails; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.ams_reg_epaymentamtpaiddetails_audit
    ADD CONSTRAINT pk_id_ams_reg_epaymentamtpaiddetails PRIMARY KEY (auditid);


--
-- Name: minutebook_data_audit pk_minutebook_data_auditid; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.minutebook_data_audit
    ADD CONSTRAINT pk_minutebook_data_auditid PRIMARY KEY (auditid);


--
-- Name: ams_reg_epaymentbankackdetails_audit pk_tranid_ams_reg_epaymentbankackdetails_audit; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.ams_reg_epaymentbankackdetails_audit
    ADD CONSTRAINT pk_tranid_ams_reg_epaymentbankackdetails_audit PRIMARY KEY (auditid);


--
-- Name: ams_reg_epaymenttransdetails_audit pk_tranid_ams_reg_epaymenttransdetails_audit; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.ams_reg_epaymenttransdetails_audit
    ADD CONSTRAINT pk_tranid_ams_reg_epaymenttransdetails_audit PRIMARY KEY (auditid);


--
-- Name: propertymaster_audit propertymaster_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.propertymaster_audit
    ADD CONSTRAINT propertymaster_audit_pkey PRIMARY KEY (auditid);


--
-- Name: propertynumberdetails_audit propertynumberdetails_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.propertynumberdetails_audit
    ADD CONSTRAINT propertynumberdetails_audit_pkey PRIMARY KEY (auditid);


--
-- Name: propertyschedules_audit propertyschedules_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.propertyschedules_audit
    ADD CONSTRAINT propertyschedules_audit_pkey PRIMARY KEY (auditid);


--
-- Name: reportmasterconfiguration_audit reportmasterconfiguration_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: postgres
--

ALTER TABLE ONLY kavericdc.reportmasterconfiguration_audit
    ADD CONSTRAINT reportmasterconfiguration_audit_pkey PRIMARY KEY (surid);


--
-- Name: sroserialmaster_audit sroserialmaster_audit_pkey; Type: CONSTRAINT; Schema: kavericdc; Owner: csgadmin
--

ALTER TABLE ONLY kavericdc.sroserialmaster_audit
    ADD CONSTRAINT sroserialmaster_audit_pkey PRIMARY KEY (auditid);


SET default_tablespace = pg_default;

--
-- Name: documentmaster_documentid_idx; Type: INDEX; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE INDEX documentmaster_documentid_idx ON kavericdc.documentmaster_audit USING btree (documentid);


--
-- Name: feesrequired_feerulecode_idx; Type: INDEX; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE INDEX feesrequired_feerulecode_idx ON kavericdc.feesrequired_audit USING btree (feerulecode);


SET default_tablespace = '';

--
-- Name: idx_ams_reg_epaymenttransdetails_appnum_audit; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_ams_reg_epaymenttransdetails_appnum_audit ON kavericdc.ams_reg_epaymenttransdetails_audit USING btree (applicationnumber);


--
-- Name: idx_ams_reg_epaymenttransdetails_chlnrefnum_audit; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_ams_reg_epaymenttransdetails_chlnrefnum_audit ON kavericdc.ams_reg_epaymenttransdetails_audit USING btree (chlnrefnum);


--
-- Name: idx_ams_reg_epaymenttransdetails_deptref_audit; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_ams_reg_epaymenttransdetails_deptref_audit ON kavericdc.ams_reg_epaymenttransdetails_audit USING btree (deptreferencecode);


--
-- Name: idx_amtpaid_audit_appno; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_amtpaid_audit_appno ON kavericdc.ams_reg_epaymentamtpaiddetails_audit USING btree (applicationnumber);


--
-- Name: idx_application_audit_logdatetime; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_application_audit_logdatetime ON kavericdc.applicantapplication_audit USING btree (logdatetime);


--
-- Name: idx_appointmentmaster_audit_appdate; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_appointmentmaster_audit_appdate ON kavericdc.appointmentmaster_audit USING btree (appointmentdate);


--
-- Name: idx_appointmentmaster_audit_appnumber; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_appointmentmaster_audit_appnumber ON kavericdc.appointmentmaster_audit USING btree (applicationnumber);


--
-- Name: idx_appointmentmaster_audit_status; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_appointmentmaster_audit_status ON kavericdc.appointmentmaster_audit USING btree (status);


--
-- Name: idx_audit_applicationnumber; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_audit_applicationnumber ON kavericdc.applicantapplication_audit USING btree (applicationnumber);


--
-- Name: idx_cc_applicationdetails_audit_appno1; Type: INDEX; Schema: kavericdc; Owner: postgres
--

CREATE INDEX idx_cc_applicationdetails_audit_appno1 ON kavericdc.cc_applicationdetails_audit USING btree (applicationnumber);


--
-- Name: idx_cc_applicationdetails_audit_ccid1; Type: INDEX; Schema: kavericdc; Owner: postgres
--

CREATE INDEX idx_cc_applicationdetails_audit_ccid1 ON kavericdc.cc_applicationdetails_audit USING btree (ccid);


--
-- Name: idx_departmentusers_service_audit; Type: INDEX; Schema: kavericdc; Owner: postgres
--

CREATE INDEX idx_departmentusers_service_audit ON kavericdc.departmentusers_audit USING btree (serviceflag);


--
-- Name: idx_departmentusers_userid_audit; Type: INDEX; Schema: kavericdc; Owner: postgres
--

CREATE INDEX idx_departmentusers_userid_audit ON kavericdc.departmentusers_audit USING btree (userid);


--
-- Name: idx_deptreferencecode_idx; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_deptreferencecode_idx ON kavericdc.ams_reg_epaymentamtpaiddetails_audit USING btree (deptreferencecode);


--
-- Name: idx_designationid_departmentusers_pkey_audit; Type: INDEX; Schema: kavericdc; Owner: postgres
--

CREATE INDEX idx_designationid_departmentusers_pkey_audit ON kavericdc.departmentusers_audit USING btree (designationid);


--
-- Name: idx_documentmaste_audit_logdatetime; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_documentmaste_audit_logdatetime ON kavericdc.documentmaster_audit USING btree (logdatetime);


--
-- Name: idx_documentmaster_audit_appno; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_documentmaster_audit_appno ON kavericdc.documentmaster_audit USING btree (applicationnumber);


--
-- Name: idx_feesrequired_audit_appno; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_feesrequired_audit_appno ON kavericdc.feesrequired_audit USING btree (applicationnumber);


--
-- Name: idx_feesrequired_audit_logdatetime; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_feesrequired_audit_logdatetime ON kavericdc.feesrequired_audit USING btree (logdatetime);


--
-- Name: idx_loginname_departmentusers_audit; Type: INDEX; Schema: kavericdc; Owner: postgres
--

CREATE INDEX idx_loginname_departmentusers_audit ON kavericdc.departmentusers_audit USING btree (loginname);


--
-- Name: idx_minutebook_data_audit_applicationnumber; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_minutebook_data_audit_applicationnumber ON kavericdc.minutebook_data_audit USING btree (applicationnumber);


--
-- Name: idx_minutebook_data_audit_appno; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_minutebook_data_audit_appno ON kavericdc.minutebook_data_audit USING btree (applicationnumber);


--
-- Name: idx_partyinfo_audit_appno1; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_partyinfo_audit_appno1 ON kavericdc.partyinfo_audit USING btree (applicationnumber);


--
-- Name: idx_partyinfo_audit_partyid1; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_partyinfo_audit_partyid1 ON kavericdc.partyinfo_audit USING btree (partyid);


--
-- Name: idx_partyinfo_fruits_audit_appno1; Type: INDEX; Schema: kavericdc; Owner: postgres
--

CREATE INDEX idx_partyinfo_fruits_audit_appno1 ON kavericdc.partyinfo_fruits_audit USING btree (applicationnumber);


--
-- Name: idx_partyinfo_fruits_audit_partyid1; Type: INDEX; Schema: kavericdc; Owner: postgres
--

CREATE INDEX idx_partyinfo_fruits_audit_partyid1 ON kavericdc.partyinfo_fruits_audit USING btree (partyid);


--
-- Name: idx_property_audit_appno; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_property_audit_appno ON kavericdc.propertymaster_audit USING btree (applicationnumber);


--
-- Name: idx_propm_audit_logdatetime; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_propm_audit_logdatetime ON kavericdc.propertymaster_audit USING btree (logdatetime);


--
-- Name: idx_propnoaudit_propertyid; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_propnoaudit_propertyid ON kavericdc.propertynumberdetails_audit USING btree (propertyid);


--
-- Name: idx_schedule_audit_appno; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_schedule_audit_appno ON kavericdc.propertyschedules_audit USING btree (applicationnumber);


--
-- Name: idx_schedule_audit_logdt; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX idx_schedule_audit_logdt ON kavericdc.propertyschedules_audit USING btree (logdatetime);


SET default_tablespace = pg_default;

--
-- Name: propertynumberdetails_propertyid_idx; Type: INDEX; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE INDEX propertynumberdetails_propertyid_idx ON kavericdc.propertynumberdetails_audit USING btree (propertyid);


SET default_tablespace = '';

--
-- Name: propertyschedules_documentid_idx; Type: INDEX; Schema: kavericdc; Owner: csgadmin
--

CREATE INDEX propertyschedules_documentid_idx ON kavericdc.propertyschedules_audit USING btree (scheduleid);


SET default_tablespace = pg_default;

--
-- Name: sroserialmaster_srocode_idx; Type: INDEX; Schema: kavericdc; Owner: csgadmin; Tablespace: pg_default
--

CREATE INDEX sroserialmaster_srocode_idx ON kavericdc.sroserialmaster_audit USING btree (srocode);


--
-- Name: appointmentmaster_audit appointmentmaster_delete; Type: RULE; Schema: kavericdc; Owner: csgadmin
--

CREATE RULE appointmentmaster_delete AS
    ON DELETE TO kavericdc.appointmentmaster_audit DO NOTHING;


--
-- Name: cc_applicationdetails_audit cc_applicationdetails_delete1; Type: RULE; Schema: kavericdc; Owner: postgres
--

CREATE RULE cc_applicationdetails_delete1 AS
    ON DELETE TO kavericdc.cc_applicationdetails_audit DO NOTHING;


--
-- Name: feesrequired_audit feesrequired_delete; Type: RULE; Schema: kavericdc; Owner: csgadmin
--

CREATE RULE feesrequired_delete AS
    ON DELETE TO kavericdc.feesrequired_audit DO NOTHING;


--
-- Name: partyinfo_audit partyinfo_delete1; Type: RULE; Schema: kavericdc; Owner: csgadmin
--

CREATE RULE partyinfo_delete1 AS
    ON DELETE TO kavericdc.partyinfo_audit DO NOTHING;


--
-- Name: partyschedules_audit partyschedules_audit_delete; Type: RULE; Schema: kavericdc; Owner: csgadmin
--

CREATE RULE partyschedules_audit_delete AS
    ON DELETE TO kavericdc.partyschedules_audit DO NOTHING;


--
-- Name: propertymaster_audit propertymaster_delete; Type: RULE; Schema: kavericdc; Owner: csgadmin
--

CREATE RULE propertymaster_delete AS
    ON DELETE TO kavericdc.propertymaster_audit DO NOTHING;


--
-- Name: propertyschedules_audit propertyschedules_delete; Type: RULE; Schema: kavericdc; Owner: csgadmin
--

CREATE RULE propertyschedules_delete AS
    ON DELETE TO kavericdc.propertyschedules_audit DO NOTHING;


--
-- Name: SCHEMA kavericdc; Type: ACL; Schema: -; Owner: csgadmin
--

GRANT ALL ON SCHEMA kavericdc TO csgkaverirwx;
GRANT ALL ON SCHEMA kavericdc TO csgcitizenuser;
GRANT ALL ON SCHEMA kavericdc TO csgdeptuser;
GRANT USAGE ON SCHEMA kavericdc TO kaveri1dept;
GRANT USAGE ON SCHEMA kavericdc TO mani;
GRANT ALL ON SCHEMA kavericdc TO sumit WITH GRANT OPTION;
GRANT ALL ON SCHEMA kavericdc TO jslip;
GRANT ALL ON SCHEMA kavericdc TO sshuser;
GRANT USAGE ON SCHEMA kavericdc TO csgk2user;
GRANT USAGE ON SCHEMA kavericdc TO shrikanth;
GRANT USAGE ON SCHEMA kavericdc TO prashanth;
GRANT USAGE ON SCHEMA kavericdc TO pavankumarhj;


--
-- Name: FUNCTION fn_ams_reg_epaymentamtpaid_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentamtpaid_audit() TO jslip;


--
-- Name: FUNCTION fn_ams_reg_epaymentbankackdetails_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymentbankackdetails_audit() TO jslip;


--
-- Name: FUNCTION fn_ams_reg_epaymenttransdetails_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_ams_reg_epaymenttransdetails_audit() TO jslip;


--
-- Name: FUNCTION fn_application_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_application_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_application_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_application_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_application_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_application_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_application_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_application_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_application_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_application_audit() TO jslip;


--
-- Name: FUNCTION fn_appointmentmaster_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_appointmentmaster_audit() TO jslip;


--
-- Name: FUNCTION fn_cc_applicationdetails_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_cc_applicationdetails_audit() TO jslip;


--
-- Name: FUNCTION fn_delete_test_data(_applicationnumber character varying); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_delete_test_data(_applicationnumber character varying) TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_delete_test_data(_applicationnumber character varying) TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_delete_test_data(_applicationnumber character varying) TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_delete_test_data(_applicationnumber character varying) TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_delete_test_data(_applicationnumber character varying) TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_delete_test_data(_applicationnumber character varying) TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_delete_test_data(_applicationnumber character varying) TO sumit WITH GRANT OPTION;


--
-- Name: FUNCTION fn_departmentusers_audit(); Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON FUNCTION kavericdc.fn_departmentusers_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_departmentusers_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_departmentusers_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_departmentusers_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_departmentusers_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_departmentusers_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_departmentusers_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_departmentusers_audit() TO sumit WITH GRANT OPTION;


--
-- Name: FUNCTION fn_documentmaster_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_documentmaster_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_documentmaster_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_documentmaster_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_documentmaster_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_documentmaster_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_documentmaster_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_documentmaster_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_documentmaster_audit() TO jslip;


--
-- Name: FUNCTION fn_eaasti_eswatuxmllog_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_eaasti_eswatuxmllog_audit() TO jslip;


--
-- Name: FUNCTION fn_ecapplicationdetals_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_ecapplicationdetals_audit() TO jslip;


--
-- Name: FUNCTION fn_feesrequired_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_feesrequired_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_feesrequired_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_feesrequired_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_feesrequired_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_feesrequired_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_feesrequired_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_feesrequired_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_feesrequired_audit() TO jslip;


--
-- Name: FUNCTION fn_insert_mdm_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_insert_mdm_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_insert_mdm_audit() TO csgdeptuser WITH GRANT OPTION;
GRANT ALL ON FUNCTION kavericdc.fn_insert_mdm_audit() TO csgk2user WITH GRANT OPTION;
GRANT ALL ON FUNCTION kavericdc.fn_insert_mdm_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_insert_mdm_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_insert_mdm_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_insert_mdm_audit() TO jslip;


--
-- Name: FUNCTION fn_minutebook_data_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_minutebook_data_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_minutebook_data_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_minutebook_data_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_minutebook_data_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_minutebook_data_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_minutebook_data_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_minutebook_data_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_minutebook_data_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_minutebook_data_audit() TO jslip;


--
-- Name: FUNCTION fn_partyinfo_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_audit() TO jslip;


--
-- Name: FUNCTION fn_partyinfo_fruits_audit(); Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_fruits_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_fruits_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_fruits_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_fruits_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_fruits_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_fruits_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_fruits_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_partyinfo_fruits_audit() TO sumit WITH GRANT OPTION;


--
-- Name: FUNCTION fn_partyschedules_fruits_audit(); Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON FUNCTION kavericdc.fn_partyschedules_fruits_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_partyschedules_fruits_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_partyschedules_fruits_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_partyschedules_fruits_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_partyschedules_fruits_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_partyschedules_fruits_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_partyschedules_fruits_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_partyschedules_fruits_audit() TO sumit WITH GRANT OPTION;


--
-- Name: FUNCTION fn_propertymaster_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_audit() TO jslip;


--
-- Name: FUNCTION fn_propertymaster_fruits_audit(); Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_fruits_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_fruits_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_fruits_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_fruits_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_fruits_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_fruits_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_fruits_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_propertymaster_fruits_audit() TO sumit WITH GRANT OPTION;


--
-- Name: FUNCTION fn_propertynumberdetails_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_propertynumberdetails_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertynumberdetails_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertynumberdetails_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_propertynumberdetails_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_propertynumberdetails_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_propertynumberdetails_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_propertynumberdetails_audit() TO jslip;


--
-- Name: FUNCTION fn_propertyschedules_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_audit() TO jslip;


--
-- Name: FUNCTION fn_propertyschedules_fruits_audit(); Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_fruits_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_fruits_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_fruits_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_fruits_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_fruits_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_fruits_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_fruits_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_propertyschedules_fruits_audit() TO sumit WITH GRANT OPTION;


--
-- Name: FUNCTION fn_reportmasterconfiguration_audit(); Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON FUNCTION kavericdc.fn_reportmasterconfiguration_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_reportmasterconfiguration_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_reportmasterconfiguration_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_reportmasterconfiguration_audit() TO csgmig;
GRANT ALL ON FUNCTION kavericdc.fn_reportmasterconfiguration_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_reportmasterconfiguration_audit() TO test_user;
GRANT ALL ON FUNCTION kavericdc.fn_reportmasterconfiguration_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_reportmasterconfiguration_audit() TO sumit WITH GRANT OPTION;


--
-- Name: FUNCTION fn_sroserialmaster_audit(); Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON FUNCTION kavericdc.fn_sroserialmaster_audit() TO csgcitizenuser;
GRANT ALL ON FUNCTION kavericdc.fn_sroserialmaster_audit() TO csgdeptuser;
GRANT ALL ON FUNCTION kavericdc.fn_sroserialmaster_audit() TO csgk2user;
GRANT ALL ON FUNCTION kavericdc.fn_sroserialmaster_audit() TO postgres;
GRANT ALL ON FUNCTION kavericdc.fn_sroserialmaster_audit() TO csgusermis;
GRANT ALL ON FUNCTION kavericdc.fn_sroserialmaster_audit() TO csgkaverirwx;
GRANT ALL ON FUNCTION kavericdc.fn_sroserialmaster_audit() TO jslip;


--
-- Name: TABLE ams_reg_epaymentamtpaiddetails_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO test_user;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO mani;
GRANT SELECT ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO postgres;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.ams_reg_epaymentamtpaiddetails_audit TO prashanth;


--
-- Name: SEQUENCE ams_reg_epaymentamtpaiddetails_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_auditid_seq TO prashanth;


--
-- Name: SEQUENCE ams_reg_epaymentamtpaiddetails_audit_id_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymentamtpaiddetails_audit_id_seq TO prashanth;


--
-- Name: TABLE ams_reg_epaymentbankackdetails_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO test_user;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO mani;
GRANT SELECT ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO postgres;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.ams_reg_epaymentbankackdetails_audit TO prashanth;


--
-- Name: SEQUENCE ams_reg_epaymentbankackdetails_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_auditid_seq TO prashanth;


--
-- Name: SEQUENCE ams_reg_epaymentbankackdetails_audit_transactionid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymentbankackdetails_audit_transactionid_seq TO prashanth;


--
-- Name: TABLE ams_reg_epaymenttransdetails_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO test_user;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO mani;
GRANT SELECT ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO postgres;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.ams_reg_epaymenttransdetails_audit TO prashanth;


--
-- Name: SEQUENCE ams_reg_epaymenttransdetails_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_auditid_seq TO prashanth;


--
-- Name: SEQUENCE ams_reg_epaymenttransdetails_audit_transactionid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.ams_reg_epaymenttransdetails_audit_transactionid_seq TO prashanth;


--
-- Name: TABLE applicantapplication_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO test_user;
GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO csgkaverirwx;
GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO postgres;
GRANT SELECT ON TABLE kavericdc.applicantapplication_audit TO kaveri1dept;
GRANT SELECT ON TABLE kavericdc.applicantapplication_audit TO mani;
GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO sumit WITH GRANT OPTION;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.applicantapplication_audit TO jslip;
GRANT ALL ON TABLE kavericdc.applicantapplication_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.applicantapplication_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.applicantapplication_audit TO prashanth;


--
-- Name: SEQUENCE applicantapplication_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.applicantapplication_audit_auditid_seq TO prashanth;


--
-- Name: TABLE appointmentmaster_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.appointmentmaster_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.appointmentmaster_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.appointmentmaster_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.appointmentmaster_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.appointmentmaster_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.appointmentmaster_audit TO test_user;
GRANT ALL ON TABLE kavericdc.appointmentmaster_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.appointmentmaster_audit TO mani;
GRANT SELECT ON TABLE kavericdc.appointmentmaster_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.appointmentmaster_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.appointmentmaster_audit TO deptdba;
GRANT ALL ON TABLE kavericdc.appointmentmaster_audit TO postgres;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.appointmentmaster_audit TO jslip;
GRANT SELECT,INSERT,UPDATE ON TABLE kavericdc.appointmentmaster_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.appointmentmaster_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.appointmentmaster_audit TO prashanth;


--
-- Name: SEQUENCE appointmentmaster_audit_appointmentid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO deptdba;
GRANT SELECT ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.appointmentmaster_audit_appointmentid_seq TO prashanth;


--
-- Name: SEQUENCE appointmentmaster_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO deptdba;
GRANT ALL ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.appointmentmaster_audit_auditid_seq TO prashanth;


--
-- Name: TABLE cc_applicationdetails_audit; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON TABLE kavericdc.cc_applicationdetails_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.cc_applicationdetails_audit TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.cc_applicationdetails_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.cc_applicationdetails_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.cc_applicationdetails_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.cc_applicationdetails_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kavericdc.cc_applicationdetails_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.cc_applicationdetails_audit TO mani;
GRANT SELECT ON TABLE kavericdc.cc_applicationdetails_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.cc_applicationdetails_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.cc_applicationdetails_audit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kavericdc.cc_applicationdetails_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.cc_applicationdetails_audit TO prashanth;


--
-- Name: SEQUENCE cc_applicationdetails_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO deptdba;
GRANT SELECT ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.cc_applicationdetails_audit_auditid_seq TO prashanth;


--
-- Name: SEQUENCE cc_applicationdetails_audit_ccid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO deptdba;
GRANT SELECT ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.cc_applicationdetails_audit_ccid_seq TO prashanth;


--
-- Name: TABLE departmentusers_audit; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON TABLE kavericdc.departmentusers_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.departmentusers_audit TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.departmentusers_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.departmentusers_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.departmentusers_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.departmentusers_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kavericdc.departmentusers_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.departmentusers_audit TO mani;
GRANT SELECT ON TABLE kavericdc.departmentusers_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.departmentusers_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.departmentusers_audit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kavericdc.departmentusers_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.departmentusers_audit TO prashanth;


--
-- Name: SEQUENCE departmentusers_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO deptdba;
GRANT SELECT ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.departmentusers_audit_auditid_seq TO prashanth;


--
-- Name: SEQUENCE departmentusers_audit_surid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_surid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.departmentusers_audit_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_surid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_surid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_surid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_surid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.departmentusers_audit_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.departmentusers_audit_surid_seq TO deptdba;


--
-- Name: SEQUENCE documentmaster_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO csgdeptuser;
GRANT ALL ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO postgres;
GRANT ALL ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.documentmaster_audit_auditid_seq TO prashanth;


--
-- Name: TABLE documentmaster_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.documentmaster_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.documentmaster_audit TO test_user;
GRANT ALL ON TABLE kavericdc.documentmaster_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.documentmaster_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.documentmaster_audit TO postgres;
GRANT ALL ON TABLE kavericdc.documentmaster_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.documentmaster_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.documentmaster_audit TO kaveri1dept;
GRANT SELECT ON TABLE kavericdc.documentmaster_audit TO mani;
GRANT ALL ON TABLE kavericdc.documentmaster_audit TO sumit WITH GRANT OPTION;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.documentmaster_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.documentmaster_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.documentmaster_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.documentmaster_audit TO prashanth;


--
-- Name: TABLE eaasti_eswatuxmllog_audit; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO mani;
GRANT SELECT ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.eaasti_eswatuxmllog_audit TO prashanth;


--
-- Name: SEQUENCE eaasti_eswatuxmllog_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO deptdba;
GRANT SELECT ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_auditid_seq TO prashanth;


--
-- Name: SEQUENCE eaasti_eswatuxmllog_audit_surid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.eaasti_eswatuxmllog_audit_surid_seq TO deptdba;


--
-- Name: TABLE ec_applicationdetails_audit; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON TABLE kavericdc.ec_applicationdetails_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.ec_applicationdetails_audit TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.ec_applicationdetails_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.ec_applicationdetails_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.ec_applicationdetails_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.ec_applicationdetails_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kavericdc.ec_applicationdetails_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.ec_applicationdetails_audit TO mani;
GRANT SELECT ON TABLE kavericdc.ec_applicationdetails_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.ec_applicationdetails_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.ec_applicationdetails_audit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kavericdc.ec_applicationdetails_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.ec_applicationdetails_audit TO prashanth;


--
-- Name: SEQUENCE ec_applicationdetails_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO deptdba;
GRANT SELECT ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.ec_applicationdetails_audit_auditid_seq TO prashanth;


--
-- Name: SEQUENCE feesrequired_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO csgdeptuser;
GRANT ALL ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO postgres;
GRANT ALL ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.feesrequired_audit_auditid_seq TO prashanth;


--
-- Name: TABLE feesrequired_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.feesrequired_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.feesrequired_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.feesrequired_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.feesrequired_audit TO postgres;
GRANT ALL ON TABLE kavericdc.feesrequired_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.feesrequired_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.feesrequired_audit TO kaveri1dept;
GRANT SELECT ON TABLE kavericdc.feesrequired_audit TO mani;
GRANT ALL ON TABLE kavericdc.feesrequired_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.feesrequired_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.feesrequired_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.feesrequired_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.feesrequired_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.feesrequired_audit TO prashanth;


--
-- Name: SEQUENCE mdm_audit_table_audit_id_seq1; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO csgdeptuser;
GRANT ALL ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO postgres;
GRANT ALL ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.mdm_audit_table_audit_id_seq1 TO prashanth;


--
-- Name: TABLE mdm_audit_table; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.mdm_audit_table TO csgk2user;
GRANT ALL ON TABLE kavericdc.mdm_audit_table TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.mdm_audit_table TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.mdm_audit_table TO csgkaverirwx;
GRANT ALL ON TABLE kavericdc.mdm_audit_table TO postgres;
GRANT ALL ON TABLE kavericdc.mdm_audit_table TO csgusermis;
GRANT SELECT ON TABLE kavericdc.mdm_audit_table TO kaveri1dept;
GRANT SELECT ON TABLE kavericdc.mdm_audit_table TO mani;
GRANT ALL ON TABLE kavericdc.mdm_audit_table TO sumit WITH GRANT OPTION;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.mdm_audit_table TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.mdm_audit_table TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.mdm_audit_table TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.mdm_audit_table TO prashanth;


--
-- Name: TABLE minutebook_data_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.minutebook_data_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.minutebook_data_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.minutebook_data_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.minutebook_data_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.minutebook_data_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.minutebook_data_audit TO test_user;
GRANT ALL ON TABLE kavericdc.minutebook_data_audit TO csgkaverirwx;
GRANT ALL ON TABLE kavericdc.minutebook_data_audit TO postgres;
GRANT SELECT ON TABLE kavericdc.minutebook_data_audit TO kaveri1dept;
GRANT SELECT ON TABLE kavericdc.minutebook_data_audit TO mani;
GRANT ALL ON TABLE kavericdc.minutebook_data_audit TO sumit WITH GRANT OPTION;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.minutebook_data_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.minutebook_data_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.minutebook_data_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.minutebook_data_audit TO prashanth;


--
-- Name: SEQUENCE minutebook_data_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.minutebook_data_audit_auditid_seq TO prashanth;


--
-- Name: SEQUENCE partyinfo_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO csgdeptuser;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO postgres;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.partyinfo_audit_auditid_seq TO prashanth;


--
-- Name: TABLE partyinfo_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.partyinfo_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.partyinfo_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.partyinfo_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.partyinfo_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.partyinfo_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.partyinfo_audit TO test_user;
GRANT ALL ON TABLE kavericdc.partyinfo_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.partyinfo_audit TO mani;
GRANT SELECT ON TABLE kavericdc.partyinfo_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.partyinfo_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.partyinfo_audit TO deptdba;
GRANT ALL ON TABLE kavericdc.partyinfo_audit TO postgres;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.partyinfo_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.partyinfo_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.partyinfo_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.partyinfo_audit TO prashanth;


--
-- Name: TABLE partyinfo_fruits_audit; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON TABLE kavericdc.partyinfo_fruits_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.partyinfo_fruits_audit TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.partyinfo_fruits_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.partyinfo_fruits_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.partyinfo_fruits_audit TO csgusermis;
GRANT SELECT,REFERENCES,TRIGGER ON TABLE kavericdc.partyinfo_fruits_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kavericdc.partyinfo_fruits_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.partyinfo_fruits_audit TO mani;
GRANT SELECT ON TABLE kavericdc.partyinfo_fruits_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.partyinfo_fruits_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.partyinfo_fruits_audit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kavericdc.partyinfo_fruits_audit TO shrikanth;


--
-- Name: SEQUENCE partyinfo_fruits_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyinfo_fruits_audit_auditid_seq TO deptdba;


--
-- Name: TABLE partyschedules_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.partyschedules_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.partyschedules_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.partyschedules_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.partyschedules_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.partyschedules_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.partyschedules_audit TO test_user;
GRANT ALL ON TABLE kavericdc.partyschedules_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.partyschedules_audit TO mani;
GRANT SELECT ON TABLE kavericdc.partyschedules_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.partyschedules_audit TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE kavericdc.partyschedules_audit TO postgres;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.partyschedules_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.partyschedules_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.partyschedules_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.partyschedules_audit TO prashanth;


--
-- Name: SEQUENCE partyschedules_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.partyschedules_audit_auditid_seq TO prashanth;


--
-- Name: SEQUENCE partyschedules_audit_partyscheduleid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.partyschedules_audit_partyscheduleid_seq TO prashanth;


--
-- Name: TABLE partyschedules_fruits_audit; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON TABLE kavericdc.partyschedules_fruits_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.partyschedules_fruits_audit TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.partyschedules_fruits_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.partyschedules_fruits_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.partyschedules_fruits_audit TO csgusermis;
GRANT SELECT,REFERENCES,TRIGGER ON TABLE kavericdc.partyschedules_fruits_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kavericdc.partyschedules_fruits_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.partyschedules_fruits_audit TO mani;
GRANT SELECT ON TABLE kavericdc.partyschedules_fruits_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.partyschedules_fruits_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.partyschedules_fruits_audit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kavericdc.partyschedules_fruits_audit TO shrikanth;


--
-- Name: SEQUENCE partyschedules_fruits_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyschedules_fruits_audit_auditid_seq TO deptdba;


--
-- Name: SEQUENCE partyschedules_fruits_audit_partyscheduleid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.partyschedules_fruits_audit_partyscheduleid_seq TO deptdba;


--
-- Name: SEQUENCE propertymaster_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO csgdeptuser;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO postgres;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.propertymaster_audit_auditid_seq TO prashanth;


--
-- Name: TABLE propertymaster_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.propertymaster_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.propertymaster_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.propertymaster_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.propertymaster_audit TO csgkaverirwx;
GRANT ALL ON TABLE kavericdc.propertymaster_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.propertymaster_audit TO test_user;
GRANT ALL ON TABLE kavericdc.propertymaster_audit TO postgres;
GRANT SELECT ON TABLE kavericdc.propertymaster_audit TO kaveri1dept;
GRANT SELECT ON TABLE kavericdc.propertymaster_audit TO mani;
GRANT ALL ON TABLE kavericdc.propertymaster_audit TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE kavericdc.propertymaster_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.propertymaster_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertymaster_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertymaster_audit TO prashanth;


--
-- Name: TABLE propertymaster_fruits_audit; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON TABLE kavericdc.propertymaster_fruits_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.propertymaster_fruits_audit TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertymaster_fruits_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.propertymaster_fruits_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.propertymaster_fruits_audit TO csgusermis;
GRANT SELECT,REFERENCES,TRIGGER ON TABLE kavericdc.propertymaster_fruits_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kavericdc.propertymaster_fruits_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.propertymaster_fruits_audit TO mani;
GRANT SELECT ON TABLE kavericdc.propertymaster_fruits_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.propertymaster_fruits_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.propertymaster_fruits_audit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertymaster_fruits_audit TO shrikanth;


--
-- Name: SEQUENCE propertymaster_fruits_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertymaster_fruits_audit_auditid_seq TO deptdba;


--
-- Name: SEQUENCE propertynumberdetails_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO csgdeptuser;
GRANT ALL ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO postgres;
GRANT ALL ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.propertynumberdetails_audit_auditid_seq TO prashanth;


--
-- Name: TABLE propertynumberdetails_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.propertynumberdetails_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.propertynumberdetails_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.propertynumberdetails_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.propertynumberdetails_audit TO postgres;
GRANT ALL ON TABLE kavericdc.propertynumberdetails_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.propertynumberdetails_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.propertynumberdetails_audit TO kaveri1dept;
GRANT SELECT ON TABLE kavericdc.propertynumberdetails_audit TO mani;
GRANT ALL ON TABLE kavericdc.propertynumberdetails_audit TO sumit WITH GRANT OPTION;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.propertynumberdetails_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.propertynumberdetails_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertynumberdetails_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertynumberdetails_audit TO prashanth;


--
-- Name: TABLE propertyschedules_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.propertyschedules_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.propertyschedules_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.propertyschedules_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.propertyschedules_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.propertyschedules_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.propertyschedules_audit TO test_user;
GRANT ALL ON TABLE kavericdc.propertyschedules_audit TO csgkaverirwx;
GRANT ALL ON TABLE kavericdc.propertyschedules_audit TO postgres;
GRANT SELECT ON TABLE kavericdc.propertyschedules_audit TO kaveri1dept;
GRANT SELECT ON TABLE kavericdc.propertyschedules_audit TO mani;
GRANT ALL ON TABLE kavericdc.propertyschedules_audit TO sumit WITH GRANT OPTION;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.propertyschedules_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.propertyschedules_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertyschedules_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertyschedules_audit TO prashanth;


--
-- Name: SEQUENCE propertyschedules_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO csgdeptuser;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO postgres;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.propertyschedules_audit_auditid_seq TO prashanth;


--
-- Name: TABLE propertyschedules_fruits_audit; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON TABLE kavericdc.propertyschedules_fruits_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.propertyschedules_fruits_audit TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertyschedules_fruits_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.propertyschedules_fruits_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.propertyschedules_fruits_audit TO csgusermis;
GRANT SELECT,REFERENCES,TRIGGER ON TABLE kavericdc.propertyschedules_fruits_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kavericdc.propertyschedules_fruits_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.propertyschedules_fruits_audit TO mani;
GRANT SELECT ON TABLE kavericdc.propertyschedules_fruits_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.propertyschedules_fruits_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.propertyschedules_fruits_audit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kavericdc.propertyschedules_fruits_audit TO shrikanth;


--
-- Name: SEQUENCE propertyschedules_fruits_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.propertyschedules_fruits_audit_auditid_seq TO deptdba;


--
-- Name: TABLE reportmasterconfiguration_audit; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON TABLE kavericdc.reportmasterconfiguration_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.reportmasterconfiguration_audit TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.reportmasterconfiguration_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.reportmasterconfiguration_audit TO csgmig;
GRANT ALL ON TABLE kavericdc.reportmasterconfiguration_audit TO csgusermis;
GRANT SELECT,REFERENCES,TRIGGER ON TABLE kavericdc.reportmasterconfiguration_audit TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kavericdc.reportmasterconfiguration_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.reportmasterconfiguration_audit TO mani;
GRANT SELECT ON TABLE kavericdc.reportmasterconfiguration_audit TO kaveri1dept;
GRANT ALL ON TABLE kavericdc.reportmasterconfiguration_audit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kavericdc.reportmasterconfiguration_audit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kavericdc.reportmasterconfiguration_audit TO shrikanth;


--
-- Name: SEQUENCE reportmasterconfiguration_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.reportmasterconfiguration_audit_auditid_seq TO deptdba;


--
-- Name: SEQUENCE reportmasterconfiguration_audit_surid_seq; Type: ACL; Schema: kavericdc; Owner: postgres
--

GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq TO csgdeptuser;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq TO csgmig;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq TO test_user;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.reportmasterconfiguration_audit_surid_seq TO deptdba;


--
-- Name: SEQUENCE sroserialmaster_audit_auditid_seq; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO csgdeptuser;
GRANT ALL ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO postgres;
GRANT ALL ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO csgusermis;
GRANT ALL ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO jslip;
GRANT SELECT,USAGE ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO sshuser;
GRANT SELECT ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO shrikanth;
GRANT SELECT ON SEQUENCE kavericdc.sroserialmaster_audit_auditid_seq TO prashanth;


--
-- Name: TABLE sroserialmaster_audit; Type: ACL; Schema: kavericdc; Owner: csgadmin
--

GRANT ALL ON TABLE kavericdc.sroserialmaster_audit TO csgk2user;
GRANT ALL ON TABLE kavericdc.sroserialmaster_audit TO csgcitizenuser;
GRANT ALL ON TABLE kavericdc.sroserialmaster_audit TO csgdeptuser;
GRANT ALL ON TABLE kavericdc.sroserialmaster_audit TO postgres;
GRANT ALL ON TABLE kavericdc.sroserialmaster_audit TO csgusermis;
GRANT ALL ON TABLE kavericdc.sroserialmaster_audit TO csgkaverirwx;
GRANT SELECT ON TABLE kavericdc.sroserialmaster_audit TO kaveri1dept;
GRANT SELECT ON TABLE kavericdc.sroserialmaster_audit TO mani;
GRANT ALL ON TABLE kavericdc.sroserialmaster_audit TO sumit WITH GRANT OPTION;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE kavericdc.sroserialmaster_audit TO jslip;
GRANT INSERT,UPDATE ON TABLE kavericdc.sroserialmaster_audit TO sshuser;
GRANT SELECT,REFERENCES ON TABLE kavericdc.sroserialmaster_audit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kavericdc.sroserialmaster_audit TO prashanth;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: kavericdc; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON SEQUENCES  TO csgcitizenuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON SEQUENCES  TO csgdeptuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT SELECT,USAGE ON SEQUENCES  TO csgk2user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON SEQUENCES  TO csgmig;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON SEQUENCES  TO csgusermis;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON SEQUENCES  TO test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON SEQUENCES  TO csgkaverirwx;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON SEQUENCES  TO sumit WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: kavericdc; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TYPES  TO csgcitizenuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TYPES  TO csgdeptuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TYPES  TO csgk2user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TYPES  TO csgmig;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TYPES  TO csgusermis;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TYPES  TO test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TYPES  TO csgkaverirwx;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TYPES  TO sumit WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: kavericdc; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON FUNCTIONS  TO csgcitizenuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON FUNCTIONS  TO csgdeptuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON FUNCTIONS  TO csgk2user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON FUNCTIONS  TO csgmig;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON FUNCTIONS  TO csgusermis;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON FUNCTIONS  TO test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON FUNCTIONS  TO csgkaverirwx;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON FUNCTIONS  TO sumit WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: kavericdc; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TABLES  TO csgcitizenuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TABLES  TO csgdeptuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT SELECT ON TABLES  TO csgk2user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TABLES  TO csgmig;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TABLES  TO csgusermis;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT SELECT,REFERENCES,TRIGGER ON TABLES  TO test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLES  TO csgkaverirwx;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT SELECT ON TABLES  TO mani;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT SELECT ON TABLES  TO kaveri1dept;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT ALL ON TABLES  TO sumit WITH GRANT OPTION;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kavericdc GRANT SELECT,REFERENCES ON TABLES  TO shrikanth;


--
-- PostgreSQL database dump complete
--

