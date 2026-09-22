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
-- Name: kaveridelapp; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA kaveridelapp;


ALTER SCHEMA kaveridelapp OWNER TO postgres;

--
-- Name: sp_delete_applications(); Type: PROCEDURE; Schema: kaveridelapp; Owner: postgres
--

CREATE PROCEDURE kaveridelapp.sp_delete_applications()
    LANGUAGE plpgsql
    AS $$
declare 
v_records record;
v_cnt int;
begin
for v_records in (select a.applicationnumber as appno,extract(days from (now()-a.inserteddatetime)) from kaveri.applicantapplicationdetails a 
left join kaveri.minutebook_data md on a.applicationnumber =md.applicationnumber
left join kaveri.withdrawapplications w on w.applicationnumber=a.applicationnumber
left join kaveri.k1pendingregistrationdata kp on kp.applicationnumber=a.applicationnumber
left join kaveri.fruits_data_recv_details fdrd on fdrd.applicationnumber=a.applicationnumber
left join kaveri.anywhere_reg_log arl  on arl.newapplicationnumber=a.applicationnumber
left join kaveri.ams_reg_epaymenttransdetails are2 on are2.applicationnumber=a.applicationnumber
where currentstatus ='CD101' and md.applicationnumber is null and w.applicationnumber is null
and fdrd.applicationnumber is null and arl.newapplicationnumber is null
and kp.applicationnumber is null and are2.applicationnumber is null and a.inserteddatetime::Date>='2025-05-01' and a.inserteddatetime::Date<(current_Date-1)
and extract(days from (now()-a.inserteddatetime))>10 order by a.inserteddatetime)
loop 

--select distinct a.applicationnumber as appno,a2.applicationnumber as appno2,extract(days from (now()-a.crtdt)) as days 
--from kaveri.applicationaudit a left join kaveri.applicationaudit a2 on a2.applicationnumber=a.applicationnumber
-- and a2.wrkflowstatusid ='CD102' 
--left join kaveri.withdrawapplications w on w.applicationnumber=a.applicationnumber
--left join kaveri.k1pendingregistrationdata kp on kp.applicationnumber=a.applicationnumber
--where a.wrkflowstatusid='CD101'and a.crtdt::date>='2023-06-01' 
--and a.crtdt::date<'2023-07-01' and a.applicationnumber like '%PRP%'
--and a2.applicationnumber is null and w.applicationnumber is null and kp.applicationnumber is null
--and extract(days from (now()-a.crtdt))>10 and a.activityorder=1
	
--select a.applicationnumber,extract(days from (now()-a.inserteddatetime)) from kaveri.applicantapplicationdetails a 
--left join kaveri.minutebook_data md on a.applicationnumber =md.applicationnumber
--left join kaveri.fruits_data_recv_details fdrd on a.applicationnumber =fdrd.applicationnumber
--left join kaveri.withdrawapplications w on w.applicationnumber=a.applicationnumber
--left join kaveri.k1pendingregistrationdata kp on kp.applicationnumber=a.applicationnumber
--where currentstatus ='CD101' and md.applicationnumber is null and fdrd.applicationnumber is null and w.applicationnumber is null
--and kp.applicationnumber is null and a.inserteddatetime::Date>='2023-06-01'
--and a.inserteddatetime::Date<'2023-07-01' and extract(days from (now()-a.inserteddatetime))>10;

	select count(*) into v_cnt from kaveridelapp.delapplicantapplicationdetails where applicationnumber =v_records.appno;

	if (v_cnt=0)
	then
		raise notice 'deleted applicationnumber %',v_records.appno;

---------------------Insertion into kaveridelapp schema-------------------------

		insert into kaveridelapp.delapplicantapplicationdetails
		select * from kaveri.applicantapplicationdetails where applicationnumber=v_records.appno; commit;
		insert into kaveridelapp.delapplicationreviewdetails
		select * from kaveri.applicationreviewdetails where applicationnumber=v_records.appno; commit;
		insert into kaveridelapp.delapplicationaudit
		select * from kaveri.applicationaudit where applicationnumber=v_records.appno; commit;
		insert into kaveridelapp.deldocumentmaster
		select * from kaveri.documentmaster where applicationnumber=v_records.appno; commit;	 
		insert into kaveridelapp.delfeesrequired
		select * from kaveri.feesrequired where applicationnumber=v_records.appno; commit;
		insert into kaveridelapp.delpropertynumberdetails
		select * from kaveri.propertynumberdetails where propertyid in (	
		select propertyid from kaveri.propertymaster where applicationnumber=v_records.appno);commit;
		insert into kaveridelapp.delpropertyschedules
		select * from kaveri.propertyschedules where applicationnumber=v_records.appno;commit;
		insert into kaveridelapp.delpropertymaster
		select * from kaveri.propertymaster where applicationnumber=v_records.appno;commit;
		insert into kaveridelapp.delpartywitness
		select * from kaveri.partywitness where partyid in (select p.partyid from kaveri.partyinfo p
				join kaveri.witnessinfo w on p.applicationnumber =w.applicationnumber 
				where p.applicationnumber=v_records.appno);commit;
		insert into kaveridelapp.delwitnessinfo
		select * from kaveri.witnessinfo w where applicationnumber=v_records.appno;commit;
		insert into kaveridelapp.delpartyinfo
		select * from kaveri.partyinfo where applicationnumber=v_records.appno;commit;
		insert into kaveridelapp.delpartyschedules
		select * from kaveri.partyschedules where applicationnumber=v_records.appno;commit;

----------------------------Deletion From Kaveri schema ---------------------------------

		delete from kaveri.partyschedules where applicationnumber=v_records.appno;commit;
		delete from kaveri.partywitness where partyid in (select p.partyid from kaveri.partyinfo p
				join kaveri.witnessinfo w on p.applicationnumber =w.applicationnumber 
				where p.applicationnumber=v_records.appno);commit;
		delete from kaveri.witnessinfo w where applicationnumber=v_records.appno;commit;
		delete from kaveri.partyinfo where applicationnumber=v_records.appno;commit;		
		delete from kaveri.propertynumberdetails where propertyid in (	
		select propertyid from kaveri.propertymaster where applicationnumber=v_records.appno);commit;
		delete from kaveri.propertyschedules where applicationnumber=v_records.appno;commit;
		delete from kaveri.propertymaster where applicationnumber=v_records.appno;commit;
		delete from kaveri.feesrequired where applicationnumber=v_records.appno;commit;
		delete from kaveri.documentmaster where applicationnumber=v_records.appno;commit;
		delete from kaveri.applicationaudit where applicationnumber=v_records.appno;commit;
		delete from kaveri.applicationreviewdetails where applicationnumber=v_records.appno;commit;
		delete from kaveri.applicantapplicationdetails where applicationnumber=v_records.appno;commit;

	end if;
end loop ;
end ;
$$;


ALTER PROCEDURE kaveridelapp.sp_delete_applications() OWNER TO postgres;

--
-- Name: sp_delete_applications_1(); Type: PROCEDURE; Schema: kaveridelapp; Owner: postgres
--

CREATE PROCEDURE kaveridelapp.sp_delete_applications_1()
    LANGUAGE plpgsql
    AS $$
declare 
v_records record;
v_cnt int;
begin
for v_records in (select applicationnumber as appno
 from kaveri.applicantapplicationdetails a  where applicationnumber in ('PRP-12082025-4516805'))
loop 

	select count(*) into v_cnt from kaveridelapp.delapplicantapplicationdetails where applicationnumber =v_records.appno;
	
	if (v_cnt=0)
	then
--		raise notice 'deleted applicationnumber %',v_records.appno;

---------------------Insertion into kaveridelapp schema-------------------------

		insert into kaveridelapp.delapplicantapplicationdetails
		select * from kaveri.applicantapplicationdetails where applicationnumber=v_records.appno; commit;
		insert into kaveridelapp.delapplicationreviewdetails
		select * from kaveri.applicationreviewdetails where applicationnumber=v_records.appno; commit;
		insert into kaveridelapp.delapplicationaudit
		select * from kaveri.applicationaudit where applicationnumber=v_records.appno; commit;
		insert into kaveridelapp.deldocumentmaster
		select * from kaveri.documentmaster where applicationnumber=v_records.appno; commit;	 
		insert into kaveridelapp.delfeesrequired
		select * from kaveri.feesrequired where applicationnumber=v_records.appno; commit;
		insert into kaveridelapp.delpropertynumberdetails
		select * from kaveri.propertynumberdetails where propertyid in (	
		select propertyid from kaveri.propertymaster where applicationnumber=v_records.appno);commit;
		insert into kaveridelapp.delpropertyschedules
		select * from kaveri.propertyschedules where applicationnumber=v_records.appno;commit;
		insert into kaveridelapp.delpropertymaster
		select * from kaveri.propertymaster where applicationnumber=v_records.appno;commit;
		insert into kaveridelapp.delpartywitness
		select * from kaveri.partywitness where partyid in (select p.partyid from kaveri.partyinfo p
				join kaveri.witnessinfo w on p.applicationnumber =w.applicationnumber 
				where p.applicationnumber=v_records.appno);commit;
		insert into kaveridelapp.delwitnessinfo
		select * from kaveri.witnessinfo w where applicationnumber=v_records.appno;commit;
		insert into kaveridelapp.delpartyinfo
		select * from kaveri.partyinfo where applicationnumber=v_records.appno;commit;
		insert into kaveridelapp.delpartyschedules
		select * from kaveri.partyschedules where applicationnumber=v_records.appno;commit;

----------------------------Deletion From Kaveri schema ---------------------------------

		delete from kaveri.partyschedules where applicationnumber=v_records.appno;commit;
		delete from kaveri.partywitness where partyid in (select p.partyid from kaveri.partyinfo p
				join kaveri.witnessinfo w on p.applicationnumber =w.applicationnumber 
				where p.applicationnumber=v_records.appno);commit;
		delete from kaveri.witnessinfo w where applicationnumber=v_records.appno;commit;
		delete from kaveri.partyinfo where applicationnumber=v_records.appno;commit;		
		delete from kaveri.propertynumberdetails where propertyid in (	
		select propertyid from kaveri.propertymaster where applicationnumber=v_records.appno);commit;
		delete from kaveri.propertyschedules where applicationnumber=v_records.appno;commit;
		delete from kaveri.propertymaster where applicationnumber=v_records.appno;commit;
		delete from kaveri.feesrequired where applicationnumber=v_records.appno;commit;
		delete from kaveri.documentmaster where applicationnumber=v_records.appno;commit;
		delete from kaveri.applicationaudit where applicationnumber=v_records.appno;commit;
		delete from kaveri.applicationreviewdetails where applicationnumber=v_records.appno;commit;
		delete from kaveri.applicantapplicationdetails where applicationnumber=v_records.appno;commit;
--		delete from kaveri.appointmentmaster  where applicationnumber=v_records.appno;commit;

	end if;
end loop ;
end ;
$$;


ALTER PROCEDURE kaveridelapp.sp_delete_applications_1() OWNER TO postgres;

--
-- Name: sp_delete_applications_by_appl(character varying); Type: PROCEDURE; Schema: kaveridelapp; Owner: raghavendrap
--

CREATE PROCEDURE kaveridelapp.sp_delete_applications_by_appl(IN _applicationnumber character varying)
    LANGUAGE plpgsql
    AS $$
declare 
v_records record;
v_cnt int;
begin

	select count(*) into v_cnt from kaveridelapp.delapplicantapplicationdetails where applicationnumber =_applicationnumber and isdeleted = true ;

	if (v_cnt=0)
	then
		raise notice 'deleted applicationnumber %',_applicationnumber;

---------------------Insertion into kaveridelapp schema-------------------------

		insert into kaveridelapp.delapplicantapplicationdetails
		select * from kaveri.applicantapplicationdetails where applicationnumber=_applicationnumber; commit;
		insert into kaveridelapp.delapplicationreviewdetails
		select * from kaveri.applicationreviewdetails where applicationnumber=_applicationnumber; commit;
		insert into kaveridelapp.delapplicationaudit
		select * from kaveri.applicationaudit where applicationnumber=_applicationnumber; commit;
		insert into kaveridelapp.deldocumentmaster
		select * from kaveri.documentmaster where applicationnumber=_applicationnumber; commit;	 
		insert into kaveridelapp.delfeesrequired
		select * from kaveri.feesrequired where applicationnumber=_applicationnumber; commit;
		insert into kaveridelapp.delpropertynumberdetails
		select * from kaveri.propertynumberdetails where propertyid in (	
		select propertyid from kaveri.propertymaster where applicationnumber=_applicationnumber);commit;
		insert into kaveridelapp.delpropertyschedules
		select * from kaveri.propertyschedules where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.delpropertymaster
		select * from kaveri.propertymaster where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.delpartywitness
		select * from kaveri.partywitness where partyid in (select p.partyid from kaveri.partyinfo p
				join kaveri.witnessinfo w on p.applicationnumber =w.applicationnumber 
				where p.applicationnumber=_applicationnumber);commit;
		insert into kaveridelapp.delwitnessinfo
		select * from kaveri.witnessinfo w where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.delpartyinfo
		select * from kaveri.partyinfo where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.delpartyschedules
		select * from kaveri.partyschedules where applicationnumber=_applicationnumber;commit;
		
		insert into kaveridelapp.delappointmentmaster
		select * from kaveri.appointmentmaster where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.delpending_flags
		select * from kaveri.pending_flags where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.delpartyesignregister
		select * from kaveri.partyesignregister where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.delorgdatajslip
		select * from kaveri.orgdatajslip where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.deldocumentsummary
		select * from kaveri.documentsummary where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.delvaluationdetails
		select * from kaveri.valuationdetails where applicationnumber=_applicationnumber;commit;
		insert into kaveridelapp.delapplicationlimitdetails
		select * from kaveri.applicationlimitdetails where applicationnumber=_applicationnumber;commit;

----------------------------Deletion From Kaveri schema ---------------------------------

		delete from kaveri.partyschedules where applicationnumber=_applicationnumber;commit;
		delete from kaveri.partywitness where partyid in (select p.partyid from kaveri.partyinfo p
				join kaveri.witnessinfo w on p.applicationnumber =w.applicationnumber 
				where p.applicationnumber=_applicationnumber);commit;
		delete from kaveri.witnessinfo w where applicationnumber=_applicationnumber;commit;
		delete from kaveri.partyinfo where applicationnumber=_applicationnumber;commit;		
		delete from kaveri.propertynumberdetails where propertyid in (	
		select propertyid from kaveri.propertymaster where applicationnumber=_applicationnumber);commit;
		delete from kaveri.propertyschedules where applicationnumber=_applicationnumber;commit;
		delete from kaveri.propertymaster where applicationnumber=_applicationnumber;commit;
		delete from kaveri.feesrequired where applicationnumber=_applicationnumber;commit;
--		delete from kaveri.fruits_data_recv_details where applicationnumber=_applicationnumber;commit;
		delete from kaveri.documentmaster where applicationnumber=_applicationnumber;commit;
		
		delete from kaveri.appointmentmaster where applicationnumber=_applicationnumber;commit;
		delete from kaveri.pending_flags where applicationnumber=_applicationnumber;commit;
		delete from kaveri.partyesignregister where applicationnumber=_applicationnumber;commit;
		delete from kaveri.orgdatajslip where applicationnumber=_applicationnumber;commit;
		delete from kaveri.documentsummary where applicationnumber=_applicationnumber;commit;
		delete from kaveri.applicationlimitdetails where applicationnumber=_applicationnumber;commit;
		delete from kaveri.valuationdetails where applicationnumber=_applicationnumber;commit;
		
		delete from kaveri.applicationaudit where applicationnumber=_applicationnumber;commit;
		delete from kaveri.applicationreviewdetails where applicationnumber=_applicationnumber;commit;
		delete from kaveri.applicantapplicationdetails where applicationnumber=_applicationnumber;commit;

	end if;
end ;
$$;


ALTER PROCEDURE kaveridelapp.sp_delete_applications_by_appl(IN _applicationnumber character varying) OWNER TO raghavendrap;

--
-- Name: sp_insert_applications(character varying); Type: PROCEDURE; Schema: kaveridelapp; Owner: raghavendrap
--

CREATE PROCEDURE kaveridelapp.sp_insert_applications(IN _applicationnumber character varying)
    LANGUAGE plpgsql
    AS $$
declare 
--v_records record;
v_cnt int;
begin

	select count(*) into v_cnt from kaveri.applicantapplicationdetails where applicationnumber =_applicationnumber;

	if (v_cnt=0)
	then
		raise notice 'Inserted applicationnumber %',_applicationnumber;

---------------------Insertion into kaveri schema-------------------------
		insert into kaveri.applicantapplicationdetails
		select * from kaveridelapp.delapplicantapplicationdetails where applicationnumber=_applicationnumber; commit;
		
		insert into kaveri.applicationreviewdetails
		select * from kaveridelapp.delapplicationreviewdetails where applicationnumber=_applicationnumber; commit;
		
		insert into kaveri.applicationaudit
		select * from kaveridelapp.delapplicationaudit where applicationnumber=_applicationnumber; commit;
		
		insert into kaveri.documentmaster
		select * from kaveridelapp.deldocumentmaster where applicationnumber=_applicationnumber; commit;	 
		
		insert into kaveri.feesrequired
		select * from kaveridelapp.delfeesrequired where applicationnumber=_applicationnumber; commit;
		
		insert into kaveri.propertynumberdetails
		select * from kaveridelapp.delpropertynumberdetails where propertyid in (	
		select propertyid from kaveridelapp.delpropertymaster where applicationnumber=_applicationnumber);commit;
		
		insert into kaveri.propertyschedules
		select * from kaveridelapp.delpropertyschedules where applicationnumber=_applicationnumber;commit;
		
		insert into kaveri.propertymaster
		select * from kaveridelapp.delpropertymaster where applicationnumber=_applicationnumber;commit;
		
		insert into kaveri.witnessinfo
		select * from kaveridelapp.delwitnessinfo w where applicationnumber=_applicationnumber;commit;
		
		insert into kaveri.partywitness
		select * from kaveridelapp.delpartywitness where partyid in (select p.partyid from kaveridelapp.delpartyinfo p
			join kaveridelapp.delwitnessinfo w on p.applicationnumber =w.applicationnumber 
			where p.applicationnumber=_applicationnumber);commit;
		
		insert into kaveri.partyinfo
		select * from kaveridelapp.delpartyinfo where applicationnumber=_applicationnumber;commit;
		
		insert into kaveri.partyschedules
		select * from kaveridelapp.delpartyschedules where applicationnumber=_applicationnumber;commit;

	end if;

end ;
$$;


ALTER PROCEDURE kaveridelapp.sp_insert_applications(IN _applicationnumber character varying) OWNER TO raghavendrap;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: delapplicantapplicationdetails; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delapplicantapplicationdetails (
    citizenid bigint,
    applicationnumber character varying(50),
    srocode integer,
    regsrocode integer,
    applicationtypeid integer,
    applicationstartdate timestamp without time zone,
    applicationenddate timestamp without time zone,
    currentstatus character varying(10),
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
    issubmitted boolean,
    isduecorrection boolean,
    ispayment boolean,
    isdueschedule boolean,
    annexurepath text,
    k1k2_flag smallint,
    inserteddatetime timestamp without time zone,
    refuseremarks text,
    remarksk text,
    isdeleted boolean,
    ispaperless boolean DEFAULT false,
    ispanverified boolean DEFAULT false,
    ispanmandatory boolean DEFAULT false,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delapplicantapplicationdetails OWNER TO postgres;

--
-- Name: delapplicantapplicationdetails_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delapplicantapplicationdetails_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delapplicantapplicationdetails_surid_seq OWNER TO postgres;

--
-- Name: delapplicantapplicationdetails_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delapplicantapplicationdetails_surid_seq OWNED BY kaveridelapp.delapplicantapplicationdetails.surid;


--
-- Name: delapplicationaudit; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delapplicationaudit (
    applicationnumber character varying(50),
    srocode integer,
    wrkflowstatusid character varying(10),
    activityby text,
    activityorder numeric(10,0),
    remarks text,
    remarks1 text,
    remarks2 text,
    crtusr character varying(10),
    crtdt timestamp without time zone,
    k1k2_flag smallint,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delapplicationaudit OWNER TO postgres;

--
-- Name: delapplicationaudit_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delapplicationaudit_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delapplicationaudit_surid_seq OWNER TO postgres;

--
-- Name: delapplicationaudit_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delapplicationaudit_surid_seq OWNED BY kaveridelapp.delapplicationaudit.surid;


--
-- Name: delapplicationlimitdetails; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delapplicationlimitdetails (
    id bigint NOT NULL,
    citizenid bigint,
    applicationnumber character varying(40),
    maxproperty integer,
    maxparty integer,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    k1k2_flag integer DEFAULT 2
);


ALTER TABLE kaveridelapp.delapplicationlimitdetails OWNER TO postgres;

--
-- Name: delapplicationlimitdetails_id_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delapplicationlimitdetails_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delapplicationlimitdetails_id_seq OWNER TO postgres;

--
-- Name: delapplicationlimitdetails_id_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delapplicationlimitdetails_id_seq OWNED BY kaveridelapp.delapplicationlimitdetails.id;


--
-- Name: delapplicationreviewdetails; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delapplicationreviewdetails (
    applicationreviewid bigint,
    reviewid integer,
    applicationnumber character varying(50),
    isverified boolean,
    remarks text,
    deptuserid bigint,
    crtdate timestamp without time zone,
    issroremarks boolean,
    k1k2_flag smallint,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delapplicationreviewdetails OWNER TO postgres;

--
-- Name: delapplicationreviewdetails_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delapplicationreviewdetails_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delapplicationreviewdetails_surid_seq OWNER TO postgres;

--
-- Name: delapplicationreviewdetails_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delapplicationreviewdetails_surid_seq OWNED BY kaveridelapp.delapplicationreviewdetails.surid;


--
-- Name: delappointmentmaster; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delappointmentmaster (
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


ALTER TABLE kaveridelapp.delappointmentmaster OWNER TO postgres;

--
-- Name: delappointmentmaster_appointmentid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delappointmentmaster_appointmentid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delappointmentmaster_appointmentid_seq OWNER TO postgres;

--
-- Name: delappointmentmaster_appointmentid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delappointmentmaster_appointmentid_seq OWNED BY kaveridelapp.delappointmentmaster.appointmentid;


--
-- Name: deldocumentmaster; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.deldocumentmaster (
    documentid bigint,
    srocode integer,
    bookid integer,
    stamparticlecode integer,
    regarticlecode integer,
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
    isxmltransferredtobhoomi boolean,
    uid integer,
    pendingdocumentnumber character varying(20),
    istransmitted boolean,
    isphotothumbtransmitted boolean,
    inserteddatetime timestamp without time zone,
    initialtransmitted boolean,
    considerationamount numeric(23,4),
    requiredstampduty numeric(23,4),
    paidstampduty numeric(23,4),
    documentstatus character varying(5),
    applicationnumber character varying(50),
    verified boolean,
    issroapproved character varying(1),
    deedattachpath character varying(200),
    ispaymentdetails boolean,
    isuploaddocuments boolean,
    uploaddocdatetime timestamp without time zone,
    registrationdatetime timestamp without time zone,
    isregistrationevaluation boolean,
    uploaddocdeedpath text,
    uploaddocannexurepath text,
    docsubmitiondate timestamp without time zone,
    lstupddate timestamp without time zone,
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
    isundervaluation boolean,
    k1k2_flag smallint,
    withdrawfilepath text,
    withdrawdocument character varying(100),
    ackdatetime timestamp without time zone,
    ackuser character varying(100),
    lateappearancepartyid bigint[],
    uploadthumbregisterpath character varying,
    isdigitallyexecuted boolean DEFAULT false,
    issignpageappended boolean DEFAULT false,
    isthumbregisterdocsigned boolean DEFAULT false,
    ispendingnoteappended boolean DEFAULT false,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.deldocumentmaster OWNER TO postgres;

--
-- Name: deldocumentmaster_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.deldocumentmaster_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.deldocumentmaster_surid_seq OWNER TO postgres;

--
-- Name: deldocumentmaster_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.deldocumentmaster_surid_seq OWNED BY kaveridelapp.deldocumentmaster.surid;


--
-- Name: deldocumentsummary; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.deldocumentsummary (
    applicationnumber character varying(100) NOT NULL,
    json_value text
);


ALTER TABLE kaveridelapp.deldocumentsummary OWNER TO postgres;

--
-- Name: deletedappno; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.deletedappno (
    applicationnumber character varying,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.deletedappno OWNER TO postgres;

--
-- Name: deletedappno_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.deletedappno_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.deletedappno_surid_seq OWNER TO postgres;

--
-- Name: deletedappno_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.deletedappno_surid_seq OWNED BY kaveridelapp.deletedappno.surid;


--
-- Name: delfeesrequired; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delfeesrequired (
    documentid bigint,
    feerulecode integer,
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
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    receiptid bigint,
    undervaluationamount numeric(23,4),
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delfeesrequired OWNER TO postgres;

--
-- Name: delfeesrequired_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delfeesrequired_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delfeesrequired_surid_seq OWNER TO postgres;

--
-- Name: delfeesrequired_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delfeesrequired_surid_seq OWNED BY kaveridelapp.delfeesrequired.surid;


--
-- Name: delorgdatajslip; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delorgdatajslip (
    mappingid integer NOT NULL,
    partyid bigint,
    documentid bigint,
    propertyid bigint,
    partytypeid integer,
    firstname character varying(1000),
    mainownerno bigint,
    ownerno bigint,
    transactextacre integer,
    transactextgunta integer,
    transactextfgunta numeric(7,5),
    applicationnumber character varying(50),
    relativename character varying(300),
    relationship character varying(100),
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE kaveridelapp.delorgdatajslip OWNER TO postgres;

--
-- Name: delpartyesignregister; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delpartyesignregister (
    id bigint NOT NULL,
    applicationnumber character varying(50),
    partyid bigint,
    docpath character varying(500),
    isbeingsigned boolean,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    iswitness boolean,
    linkid character varying,
    documentid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delpartyesignregister OWNER TO postgres;

--
-- Name: delpartyesignregister_id_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delpartyesignregister_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delpartyesignregister_id_seq OWNER TO postgres;

--
-- Name: delpartyesignregister_id_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delpartyesignregister_id_seq OWNED BY kaveridelapp.delpartyesignregister.id;


--
-- Name: delpartyesignregister_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delpartyesignregister_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delpartyesignregister_surid_seq OWNER TO postgres;

--
-- Name: delpartyesignregister_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delpartyesignregister_surid_seq OWNED BY kaveridelapp.delpartyesignregister.surid;


--
-- Name: delpartyinfo; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delpartyinfo (
    partyid bigint,
    srocode integer,
    documentid bigint,
    partytypeid integer,
    firstname character varying(300),
    middlename character varying(300),
    lastname character varying(350),
    address character varying(300),
    age character varying(3),
    sex smallint,
    isexecutor boolean,
    ispresenter boolean,
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
    isorganization boolean,
    organizationid integer,
    applicationnumber character varying(50),
    verified boolean,
    issroapproved character varying(1),
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
    isprivateattendance boolean,
    coveringletterno character(100),
    section88file character(500),
    isendorseprinted boolean,
    thumbremarks character varying(200),
    partyidreference bigint,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    ispartyrefused boolean,
    islateapperance boolean,
    isduplicate boolean,
    duplicatepartyid bigint,
    presenternamee character varying(100),
    isbiometricrefused boolean,
    iscitizennotappeared boolean,
    aadharhash character varying(500),
    datetimeofconsent character varying,
    nameasperaadhar character varying(500),
    digilockerid character varying,
    isdeptaadharvalidated boolean,
    iscitizenaadharverified boolean,
    aadhaar_decline_reason character varying,
    aadhaardeclinereason character varying,
    idcardhash text,
    isdocumentexecuted boolean DEFAULT false,
    isendorsementsigned boolean DEFAULT false,
    isthumbregistersigned boolean DEFAULT false,
    namematchpercentage integer,
    ispartypanverified boolean DEFAULT false,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delpartyinfo OWNER TO postgres;

--
-- Name: delpartyinfo_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delpartyinfo_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delpartyinfo_surid_seq OWNER TO postgres;

--
-- Name: delpartyinfo_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delpartyinfo_surid_seq OWNED BY kaveridelapp.delpartyinfo.surid;


--
-- Name: delpartyschedules; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delpartyschedules (
    partyscheduleid bigint,
    partyid bigint,
    scheduleid bigint,
    propertyid bigint,
    applicationnumber character varying(50),
    isdelete boolean,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delpartyschedules OWNER TO postgres;

--
-- Name: delpartyschedules_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delpartyschedules_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delpartyschedules_surid_seq OWNER TO postgres;

--
-- Name: delpartyschedules_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delpartyschedules_surid_seq OWNED BY kaveridelapp.delpartyschedules.surid;


--
-- Name: delpartywitness; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delpartywitness (
    partyid bigint,
    witnessid bigint,
    witnessdate timestamp without time zone,
    srocode integer,
    k1k2_flag smallint,
    inserteddatetime timestamp without time zone,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delpartywitness OWNER TO postgres;

--
-- Name: delpartywitness_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delpartywitness_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delpartywitness_surid_seq OWNER TO postgres;

--
-- Name: delpartywitness_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delpartywitness_surid_seq OWNED BY kaveridelapp.delpartywitness.surid;


--
-- Name: delpending_flags; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delpending_flags (
    applicationnumber character varying(255) NOT NULL,
    isimpound boolean,
    isundervaluation boolean,
    isdelaycondonation boolean,
    ispartylateappearance boolean,
    isprivateatteandace boolean
);


ALTER TABLE kaveridelapp.delpending_flags OWNER TO postgres;

--
-- Name: delpropertymaster; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delpropertymaster (
    propertyid bigint,
    documentid bigint,
    villagecode bigint,
    regsrocode integer,
    srocode integer,
    totalarea numeric(20,6),
    unitid integer,
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
    ismovableproperty boolean,
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
    verified boolean,
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
    inserteddatetime timestamp without time zone,
    zoneid integer,
    subpropertytypeid integer,
    k1k2_flag smallint,
    sroroadcode bigint,
    sfdaroadcode bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delpropertymaster OWNER TO postgres;

--
-- Name: delpropertymaster_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delpropertymaster_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delpropertymaster_surid_seq OWNER TO postgres;

--
-- Name: delpropertymaster_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delpropertymaster_surid_seq OWNED BY kaveridelapp.delpropertymaster.surid;


--
-- Name: delpropertynumberdetails; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delpropertynumberdetails (
    propertyid bigint,
    srocode integer,
    currentpropertytypeid integer,
    currentnumber character varying(100),
    oldpropertytypeid integer,
    oldnumber character varying(75),
    description character varying(1000),
    survey_no integer,
    surnoc character varying(20),
    hissa_no character varying(30),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delpropertynumberdetails OWNER TO postgres;

--
-- Name: delpropertynumberdetails_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delpropertynumberdetails_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delpropertynumberdetails_surid_seq OWNER TO postgres;

--
-- Name: delpropertynumberdetails_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delpropertynumberdetails_surid_seq OWNED BY kaveridelapp.delpropertynumberdetails.surid;


--
-- Name: delpropertyschedules; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delpropertyschedules (
    scheduleid bigint,
    propertyid bigint,
    srocode integer,
    partyid bigint,
    scheduletype character varying(6),
    totalarea numeric(20,6),
    unitid integer,
    description character varying(5000),
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
    verified boolean,
    issroapproved character varying(1),
    eastboundary character varying(500),
    westboundary character varying(500),
    northboundary character varying(500),
    southboundary character varying(500),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    electriccompid character varying(100),
    waterboardid character varying(100),
    electriccomp integer,
    waterboard integer,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delpropertyschedules OWNER TO postgres;

--
-- Name: delpropertyschedules_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delpropertyschedules_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delpropertyschedules_surid_seq OWNER TO postgres;

--
-- Name: delpropertyschedules_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delpropertyschedules_surid_seq OWNED BY kaveridelapp.delpropertyschedules.surid;


--
-- Name: delvaluationdetails; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delvaluationdetails (
    valid bigint NOT NULL,
    srocode integer NOT NULL,
    regsrocode integer NOT NULL,
    villagecode bigint,
    roadcode integer,
    valuationdate timestamp without time zone,
    propertytypeid integer,
    totalarea numeric(18,4),
    unitid integer,
    marketvalue numeric,
    leasetype integer,
    leaseamount numeric,
    northboundary character varying(50),
    southboundary character varying(50),
    eastboundary character varying(50),
    westboundary character varying(50),
    assessment character varying(2000),
    regarticlecode integer,
    applicationnumber character varying(50),
    verified boolean DEFAULT false,
    issroapproved character varying(1) DEFAULT 'E'::character varying,
    propertyid bigint,
    reportdetails character varying,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE kaveridelapp.delvaluationdetails OWNER TO postgres;

--
-- Name: delwitnessinfo; Type: TABLE; Schema: kaveridelapp; Owner: postgres
--

CREATE TABLE kaveridelapp.delwitnessinfo (
    witnessid bigint,
    documentid bigint,
    name character varying(500),
    address character varying(500),
    sex integer,
    age character varying(3),
    profession character varying(150),
    registrationid bigint,
    dateofbirth timestamp without time zone,
    status character varying(15),
    phoneno character varying(20),
    relation character varying(50),
    mothername character varying(50),
    fathersname character varying(50),
    presentatsolemanization character(10),
    srocode integer,
    isonline boolean,
    applicationnumber character varying(50),
    verified boolean,
    issroapproved character varying(1),
    statecode integer,
    districtcode integer,
    talukcode integer,
    hoblicode integer,
    villagecode bigint,
    relativename character varying(200),
    pincode integer,
    middlename text,
    lastname text,
    houseno text,
    iscliment boolean,
    isexicutent boolean,
    isendorseprinted boolean,
    ispresentverification boolean,
    k1k2_flag smallint,
    inserteddatetime timestamp without time zone,
    isdocumentexecuted boolean DEFAULT false,
    isendorsementsigned boolean DEFAULT false,
    isthumbregistersigned boolean DEFAULT false,
    surid bigint NOT NULL
);


ALTER TABLE kaveridelapp.delwitnessinfo OWNER TO postgres;

--
-- Name: delwitnessinfo_surid_seq; Type: SEQUENCE; Schema: kaveridelapp; Owner: postgres
--

CREATE SEQUENCE kaveridelapp.delwitnessinfo_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaveridelapp.delwitnessinfo_surid_seq OWNER TO postgres;

--
-- Name: delwitnessinfo_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaveridelapp; Owner: postgres
--

ALTER SEQUENCE kaveridelapp.delwitnessinfo_surid_seq OWNED BY kaveridelapp.delwitnessinfo.surid;


--
-- Name: delapplicantapplicationdetails surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delapplicantapplicationdetails ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delapplicantapplicationdetails_surid_seq'::regclass);


--
-- Name: delapplicationaudit surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delapplicationaudit ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delapplicationaudit_surid_seq'::regclass);


--
-- Name: delapplicationlimitdetails id; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delapplicationlimitdetails ALTER COLUMN id SET DEFAULT nextval('kaveridelapp.delapplicationlimitdetails_id_seq'::regclass);


--
-- Name: delapplicationreviewdetails surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delapplicationreviewdetails ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delapplicationreviewdetails_surid_seq'::regclass);


--
-- Name: delappointmentmaster appointmentid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delappointmentmaster ALTER COLUMN appointmentid SET DEFAULT nextval('kaveridelapp.delappointmentmaster_appointmentid_seq'::regclass);


--
-- Name: deldocumentmaster surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.deldocumentmaster ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.deldocumentmaster_surid_seq'::regclass);


--
-- Name: deletedappno surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.deletedappno ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.deletedappno_surid_seq'::regclass);


--
-- Name: delfeesrequired surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delfeesrequired ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delfeesrequired_surid_seq'::regclass);


--
-- Name: delpartyesignregister id; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpartyesignregister ALTER COLUMN id SET DEFAULT nextval('kaveridelapp.delpartyesignregister_id_seq'::regclass);


--
-- Name: delpartyesignregister surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpartyesignregister ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delpartyesignregister_surid_seq'::regclass);


--
-- Name: delpartyinfo surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpartyinfo ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delpartyinfo_surid_seq'::regclass);


--
-- Name: delpartyschedules surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpartyschedules ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delpartyschedules_surid_seq'::regclass);


--
-- Name: delpartywitness surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpartywitness ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delpartywitness_surid_seq'::regclass);


--
-- Name: delpropertymaster surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpropertymaster ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delpropertymaster_surid_seq'::regclass);


--
-- Name: delpropertynumberdetails surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpropertynumberdetails ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delpropertynumberdetails_surid_seq'::regclass);


--
-- Name: delpropertyschedules surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpropertyschedules ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delpropertyschedules_surid_seq'::regclass);


--
-- Name: delwitnessinfo surid; Type: DEFAULT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delwitnessinfo ALTER COLUMN surid SET DEFAULT nextval('kaveridelapp.delwitnessinfo_surid_seq'::regclass);


--
-- Name: delapplicationlimitdetails applicationlimitdetails_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delapplicationlimitdetails
    ADD CONSTRAINT applicationlimitdetails_pkey PRIMARY KEY (id);


--
-- Name: delappointmentmaster appointmentmaster_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delappointmentmaster
    ADD CONSTRAINT appointmentmaster_pkey PRIMARY KEY (appointmentid);


--
-- Name: delapplicantapplicationdetails delapplicantapplicationdetails_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delapplicantapplicationdetails
    ADD CONSTRAINT delapplicantapplicationdetails_pkey PRIMARY KEY (surid);


--
-- Name: delapplicationaudit delapplicationaudit_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delapplicationaudit
    ADD CONSTRAINT delapplicationaudit_pkey PRIMARY KEY (surid);


--
-- Name: delapplicationreviewdetails delapplicationreviewdetails_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delapplicationreviewdetails
    ADD CONSTRAINT delapplicationreviewdetails_pkey PRIMARY KEY (surid);


--
-- Name: deldocumentmaster deldocumentmaster_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.deldocumentmaster
    ADD CONSTRAINT deldocumentmaster_pkey PRIMARY KEY (surid);


--
-- Name: deletedappno deletedappno_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.deletedappno
    ADD CONSTRAINT deletedappno_pkey PRIMARY KEY (surid);


--
-- Name: delfeesrequired delfeesrequired_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delfeesrequired
    ADD CONSTRAINT delfeesrequired_pkey PRIMARY KEY (surid);


--
-- Name: delpartyesignregister delpartyesignregister_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpartyesignregister
    ADD CONSTRAINT delpartyesignregister_pkey PRIMARY KEY (surid);


--
-- Name: delpartyinfo delpartyinfo_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpartyinfo
    ADD CONSTRAINT delpartyinfo_pkey PRIMARY KEY (surid);


--
-- Name: delpartyschedules delpartyschedules_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpartyschedules
    ADD CONSTRAINT delpartyschedules_pkey PRIMARY KEY (surid);


--
-- Name: delpartywitness delpartywitness_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpartywitness
    ADD CONSTRAINT delpartywitness_pkey PRIMARY KEY (surid);


--
-- Name: delpropertymaster delpropertymaster_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpropertymaster
    ADD CONSTRAINT delpropertymaster_pkey PRIMARY KEY (surid);


--
-- Name: delpropertynumberdetails delpropertynumberdetails_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpropertynumberdetails
    ADD CONSTRAINT delpropertynumberdetails_pkey PRIMARY KEY (surid);


--
-- Name: delpropertyschedules delpropertyschedules_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpropertyschedules
    ADD CONSTRAINT delpropertyschedules_pkey PRIMARY KEY (surid);


--
-- Name: delwitnessinfo delwitnessinfo_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delwitnessinfo
    ADD CONSTRAINT delwitnessinfo_pkey PRIMARY KEY (surid);


--
-- Name: delpending_flags pending_flags_pkey; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delpending_flags
    ADD CONSTRAINT pending_flags_pkey PRIMARY KEY (applicationnumber);


--
-- Name: deldocumentsummary pk_documentsummary_applicationnumber; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.deldocumentsummary
    ADD CONSTRAINT pk_documentsummary_applicationnumber PRIMARY KEY (applicationnumber);


--
-- Name: delorgdatajslip pk_orgdatajslip_mappingid; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delorgdatajslip
    ADD CONSTRAINT pk_orgdatajslip_mappingid PRIMARY KEY (mappingid);


--
-- Name: delvaluationdetails pk_valdtls_validregsrocd; Type: CONSTRAINT; Schema: kaveridelapp; Owner: postgres
--

ALTER TABLE ONLY kaveridelapp.delvaluationdetails
    ADD CONSTRAINT pk_valdtls_validregsrocd PRIMARY KEY (valid, regsrocode);


--
-- Name: SCHEMA kaveridelapp; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA kaveridelapp TO shrikanth;
GRANT USAGE ON SCHEMA kaveridelapp TO prashanth;


--
-- Name: PROCEDURE sp_delete_applications(); Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT ALL ON PROCEDURE kaveridelapp.sp_delete_applications() TO sumit WITH GRANT OPTION;


--
-- Name: PROCEDURE sp_delete_applications_1(); Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT ALL ON PROCEDURE kaveridelapp.sp_delete_applications_1() TO sumit WITH GRANT OPTION;


--
-- Name: TABLE delapplicantapplicationdetails; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicantapplicationdetails TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delapplicantapplicationdetails TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delapplicantapplicationdetails TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicantapplicationdetails TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicantapplicationdetails TO prashanth;


--
-- Name: SEQUENCE delapplicantapplicationdetails_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delapplicantapplicationdetails_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicantapplicationdetails_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delapplicantapplicationdetails_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicantapplicationdetails_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicantapplicationdetails_surid_seq TO csgdeptuser;


--
-- Name: TABLE delapplicationaudit; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicationaudit TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delapplicationaudit TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delapplicationaudit TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicationaudit TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicationaudit TO prashanth;


--
-- Name: SEQUENCE delapplicationaudit_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delapplicationaudit_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicationaudit_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delapplicationaudit_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicationaudit_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicationaudit_surid_seq TO csgdeptuser;


--
-- Name: TABLE delapplicationlimitdetails; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicationlimitdetails TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delapplicationlimitdetails TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delapplicationlimitdetails TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicationlimitdetails TO shrikanth;


--
-- Name: SEQUENCE delapplicationlimitdetails_id_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delapplicationlimitdetails_id_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicationlimitdetails_id_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delapplicationlimitdetails_id_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicationlimitdetails_id_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicationlimitdetails_id_seq TO csgdeptuser;


--
-- Name: TABLE delapplicationreviewdetails; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicationreviewdetails TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delapplicationreviewdetails TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delapplicationreviewdetails TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicationreviewdetails TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delapplicationreviewdetails TO prashanth;


--
-- Name: SEQUENCE delapplicationreviewdetails_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delapplicationreviewdetails_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicationreviewdetails_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delapplicationreviewdetails_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicationreviewdetails_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delapplicationreviewdetails_surid_seq TO csgdeptuser;


--
-- Name: TABLE delappointmentmaster; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delappointmentmaster TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delappointmentmaster TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delappointmentmaster TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delappointmentmaster TO shrikanth;


--
-- Name: SEQUENCE delappointmentmaster_appointmentid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delappointmentmaster_appointmentid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delappointmentmaster_appointmentid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delappointmentmaster_appointmentid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delappointmentmaster_appointmentid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delappointmentmaster_appointmentid_seq TO csgdeptuser;


--
-- Name: TABLE deldocumentmaster; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.deldocumentmaster TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.deldocumentmaster TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.deldocumentmaster TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.deldocumentmaster TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.deldocumentmaster TO prashanth;


--
-- Name: SEQUENCE deldocumentmaster_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.deldocumentmaster_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.deldocumentmaster_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.deldocumentmaster_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.deldocumentmaster_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.deldocumentmaster_surid_seq TO csgdeptuser;


--
-- Name: TABLE deldocumentsummary; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.deldocumentsummary TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.deldocumentsummary TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.deldocumentsummary TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.deldocumentsummary TO shrikanth;


--
-- Name: TABLE deletedappno; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.deletedappno TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.deletedappno TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.deletedappno TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.deletedappno TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.deletedappno TO prashanth;


--
-- Name: SEQUENCE deletedappno_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.deletedappno_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.deletedappno_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.deletedappno_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.deletedappno_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.deletedappno_surid_seq TO csgdeptuser;


--
-- Name: TABLE delfeesrequired; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delfeesrequired TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delfeesrequired TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delfeesrequired TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delfeesrequired TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delfeesrequired TO prashanth;


--
-- Name: SEQUENCE delfeesrequired_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delfeesrequired_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delfeesrequired_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delfeesrequired_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delfeesrequired_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delfeesrequired_surid_seq TO csgdeptuser;


--
-- Name: TABLE delorgdatajslip; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delorgdatajslip TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delorgdatajslip TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delorgdatajslip TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delorgdatajslip TO shrikanth;


--
-- Name: TABLE delpartyesignregister; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartyesignregister TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delpartyesignregister TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delpartyesignregister TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartyesignregister TO shrikanth;


--
-- Name: SEQUENCE delpartyesignregister_id_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delpartyesignregister_id_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyesignregister_id_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delpartyesignregister_id_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyesignregister_id_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyesignregister_id_seq TO csgdeptuser;


--
-- Name: SEQUENCE delpartyesignregister_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delpartyesignregister_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyesignregister_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delpartyesignregister_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyesignregister_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyesignregister_surid_seq TO csgdeptuser;


--
-- Name: TABLE delpartyinfo; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartyinfo TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delpartyinfo TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delpartyinfo TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartyinfo TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartyinfo TO prashanth;


--
-- Name: SEQUENCE delpartyinfo_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delpartyinfo_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyinfo_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delpartyinfo_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyinfo_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyinfo_surid_seq TO csgdeptuser;


--
-- Name: TABLE delpartyschedules; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartyschedules TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delpartyschedules TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delpartyschedules TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartyschedules TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartyschedules TO prashanth;


--
-- Name: SEQUENCE delpartyschedules_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delpartyschedules_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyschedules_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delpartyschedules_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyschedules_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delpartyschedules_surid_seq TO csgdeptuser;


--
-- Name: TABLE delpartywitness; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartywitness TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delpartywitness TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delpartywitness TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartywitness TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpartywitness TO prashanth;


--
-- Name: SEQUENCE delpartywitness_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delpartywitness_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delpartywitness_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delpartywitness_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delpartywitness_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delpartywitness_surid_seq TO csgdeptuser;


--
-- Name: TABLE delpending_flags; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpending_flags TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delpending_flags TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delpending_flags TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpending_flags TO shrikanth;


--
-- Name: TABLE delpropertymaster; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpropertymaster TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delpropertymaster TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delpropertymaster TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpropertymaster TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpropertymaster TO prashanth;


--
-- Name: SEQUENCE delpropertymaster_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delpropertymaster_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delpropertymaster_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delpropertymaster_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delpropertymaster_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delpropertymaster_surid_seq TO csgdeptuser;


--
-- Name: TABLE delpropertynumberdetails; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpropertynumberdetails TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delpropertynumberdetails TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delpropertynumberdetails TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpropertynumberdetails TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpropertynumberdetails TO prashanth;


--
-- Name: SEQUENCE delpropertynumberdetails_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delpropertynumberdetails_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delpropertynumberdetails_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delpropertynumberdetails_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delpropertynumberdetails_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delpropertynumberdetails_surid_seq TO csgdeptuser;


--
-- Name: TABLE delpropertyschedules; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpropertyschedules TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delpropertyschedules TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delpropertyschedules TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpropertyschedules TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delpropertyschedules TO prashanth;


--
-- Name: SEQUENCE delpropertyschedules_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delpropertyschedules_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delpropertyschedules_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delpropertyschedules_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delpropertyschedules_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delpropertyschedules_surid_seq TO csgdeptuser;


--
-- Name: TABLE delvaluationdetails; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delvaluationdetails TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delvaluationdetails TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delvaluationdetails TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delvaluationdetails TO shrikanth;


--
-- Name: TABLE delwitnessinfo; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delwitnessinfo TO csgk2user;
GRANT ALL ON TABLE kaveridelapp.delwitnessinfo TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE kaveridelapp.delwitnessinfo TO deptdba;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delwitnessinfo TO shrikanth;
GRANT SELECT,REFERENCES ON TABLE kaveridelapp.delwitnessinfo TO prashanth;


--
-- Name: SEQUENCE delwitnessinfo_surid_seq; Type: ACL; Schema: kaveridelapp; Owner: postgres
--

GRANT SELECT ON SEQUENCE kaveridelapp.delwitnessinfo_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaveridelapp.delwitnessinfo_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaveridelapp.delwitnessinfo_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaveridelapp.delwitnessinfo_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaveridelapp.delwitnessinfo_surid_seq TO csgdeptuser;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: kaveridelapp; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaveridelapp GRANT SELECT,REFERENCES ON TABLES  TO shrikanth;


--
-- PostgreSQL database dump complete
--

