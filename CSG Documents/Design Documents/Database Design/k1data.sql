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
-- Name: k1data; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA k1data;


ALTER SCHEMA k1data OWNER TO postgres;

--
-- Name: k1ec_srch_property; Type: TYPE; Schema: k1data; Owner: postgres
--

CREATE TYPE k1data.k1ec_srch_property AS (
	_currentproperttypeid bigint,
	_currentnumber character varying
);


ALTER TYPE k1data.k1ec_srch_property OWNER TO postgres;

--
-- Name: fn_ec_prptysch_k1(bigint, integer); Type: FUNCTION; Schema: k1data; Owner: postgres
--

CREATE FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) RETURNS TABLE(scheduleid bigint, easttowest character varying, northtosouth character varying, description character varying)
    LANGUAGE plpgsql
    AS $$
 
begin

return query
select 
ps.scheduleid,
ps.easttowest,
ps.northtosouth,
case when ps.propertyid is not null 
then
case when  ps.description is not null and  ps.description<>'' then  
concat(ps.description,'')
else concat('District: ', d.districtnamee,', ' , 'Taluk: ', tm.taluknamee,', ' , 'Village: ',v2.villagenamee,', ', '', 'Survey No: ',pnd.survey_no
,', ', 'Hissa No: ', pnd.hissa_no,', '
, 'BoundaryDetails: [North: ',ps.northboundary,', '
, 'East: ',ps.eastboundary,', '
, 'West: ', ps.westboundary,', ', 'South: ', ps.southboundary,', ','] measuring '
,ps.totalarea,' acre') end 
else
ps.description end as
description
from k1data.propertymaster pm 
join k1data.propertyschedules ps on pm.propertyid=ps.propertyid and ps.srocode =pm.regsrocode 
join k1data.propertynumberdetails pnd on ps.propertyid=pnd.propertyid and pm.regsrocode =pnd.srocode
left join k1data.partyinfo pf on  pm.documentid=pf.documentid and pm.srocode=pf.srocode
--join k1data.villagemastervillagesmergingmappping vm on vm.villagecode=pm.villagecode
join k1data.villagemaster v2 on v2.villagecode=pm.villagecode
join k1data.talukmaster tm on v2.talukcode =tm.talukcode  
join k1data.districtmaster d on tm.districtcode =d.districtcode
where pm.propertyid=_propertyid and pm.srocode=_srocode
group by ps.easttowest, ps.northtosouth,ps.description,ps.propertyid
,d.districtnamee,tm.taluknamee,v2.villagenamee,pnd.survey_no,pnd.hissa_no,ps.northboundary
,ps.eastboundary,ps.westboundary,ps.southboundary,ps.totalarea,ps.scheduleid
;
end;
$$;


ALTER FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) OWNER TO postgres;

--
-- Name: fn_fetch_ecdocid_k1(integer, k1data.k1ec_srch_property[], timestamp without time zone, timestamp without time zone); Type: FUNCTION; Schema: k1data; Owner: postgres
--

CREATE FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) RETURNS TABLE(documentid bigint, srocode integer, propertyid bigint)
    LANGUAGE plpgsql
    AS $$
begin
--return query
--SELECT distinct DM.DocumentID,DM.SROCode 
--FROM k1data.DOCUMENTMASTER DM
--  left JOIN k1data.ECPropertySearchKeyValues PM ON PM.DOCUMENTID = DM.DocumentID
--  AND PM.RegSROCode = DM.SROCODE
--  left join k1data.DEC_DROrderMaster OM ON PM.DOCUMENTID = DM.DocumentID and  OM.SROCode = DM.SROCODE
--  AND OM.DocumentID = DM.DocumentID
--  and OM.IsFinalized = 1
--  INNER JOIN k1data.villagemastervillagesmergingmappping TVM ON PM.VillageCode = TVM.VillageCode
--  join (select distinct propertyid from k1data.PropertyNumberDetails pn 
--        where currentnumber in (select currentnumber 
--	        from unnest(p_srch_property)) and currentpropertytypeid in (select currentpropertytypeid 
--	        from unnest(p_srch_property)))pnd on pnd.propertyid=pm.propertyid 
--WHERE DM.registrationdatetime IS NOT NULL
--  AND DM.registrationdatetime::date >= _fromdate
--  AND DM.registrationdatetime::date <=_todate
--  and pm.villagecode=_villagecode
--  and pm.IsActivated = 1;

--SELECT distinct DM.DocumentID,DM.SROCode 
--FROM k1data.DOCUMENTMASTER DM
--  left JOIN ECPropertySearchKeyValues PM ON PM.DOCUMENTID = DM.DocumentID
--  AND PM.RegSROCode = DM.SROCODE
--  left join DEC_DROrderMaster OM ON PM.DOCUMENTID = DM.DocumentID and  OM.SROCode = DM.SROCODE
--  AND OM.DocumentID = DM.DocumentID
--  and OM.IsFinalized = 1
--  INNER JOIN k1data.villagemastervillagesmergingmappping TVM ON PM.VillageCode = TVM.VillageCode
--  join (select distinct propertyid from k1data.PropertyNumberDetails pn 
--        where (currentnumber,currentpropertytypeid) in (select currentnumber,currentpropertytypeid 
--        from unnest(p_srch_property)))pnd on pnd.propertyid=pm.propertyid 
--WHERE DM.registrationdatetime IS NOT NULL
--  AND DM.registrationdatetime >= _fromdate
--  AND DM.registrationdatetime < DATEADD(DAY, 1,_todate)
--  and pm.villagecode=_villagecode
--  and pm.IsActivated = 1;

--return query
-- SELECT distinct DM.DocumentID,DM.SROCode 
--FROM k1data.DOCUMENTMASTER DM
--  left JOIN k1data.ECPropertySearchKeyValues PM ON PM.DOCUMENTID = DM.DocumentID
--  AND PM.regsrocode = DM.SROCODE
--  left join k1data.DEC_DROrderMaster OM ON OM.DOCUMENTID = DM.DocumentID and  OM.SROCode = DM.SROCODE and OM.IsFinalized = 1
--left JOIN k1data.villagemastervillagesmergingmappping TVM ON PM.VillageCode = TVM.VillageCode
--join k1data.PropertyNumberDetails pnd on pnd.propertyid=pm.propertyid and pnd.srocode =pm.regsrocode 
--WHERE DM.registrationdatetime IS NOT NULL
--  AND DM.stamp5datetime::date >= _fromdate
--  AND DM.stamp5datetime::date <=_todate
--  and pm.villagecode=_villagecode
--  and pm.IsActivated = 1 and (pnd.currentnumber,pnd.currentpropertytypeid) in (select pn._currentnumber,pn._currentproperttypeid 
--        from unnest(p_srch_property) as pn) ;


return query
SELECT distinct PM.DocumentID,PM.SROCode ,PM.propertyid
FROM k1data.ECPropertySearchKeyValues PM 
join k1data.documentmaster dm on pm.documentid =dm.documentid and pm.srocode=dm.srocode
left JOIN k1data.villagemastervillagesmergingmappping vm ON PM.VillageCode = VM.VillageCode
WHERE pm.villagecode=_villagecode 
  and pm.IsActivated = 1 and (pm.currentnumber,pm.currentpropertytypeid) in (select pn._currentnumber,pn._currentproperttypeid 
        from unnest(p_srch_property) as pn)
 and dm.registrationdatetime::date>=_fromdate and dm.registrationdatetime<=_todate;




end;
$$;


ALTER FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) OWNER TO postgres;

--
-- Name: fn_fetch_ecjson_chk_docdetails_k1(bigint, bigint); Type: FUNCTION; Schema: k1data; Owner: postgres
--

CREATE FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) RETURNS TABLE(applicationnumber character varying, propertyid bigint, marketvalue numeric, consideration numeric, articlenamee character varying, east character varying, west character varying, north character varying, south character varying, area numeric, villagecode bigint, villagenamee character varying, hoblicode integer, hoblinamee character varying, referencetext character varying, documentid bigint, srocode integer, executiondate timestamp without time zone, cdnumber character varying, pagecount integer, documentreference character varying, note_enteredpart character varying, liabilitynote text)
    LANGUAGE plpgsql
    AS $$
begin 

return query 
select 
pm.applicationnumber,pm.propertyid,pm.marketvalue,pm.sroconsideration as consideration,ra.articlenamee,pm.eastboundary AS east,pm.westboundary AS west,
pm.northboundary AS north,pm.southboundary AS south,pm.totalarea AS area,pm.villagecode,v.villagenamee,v.hoblicode,
h.hoblinamee,
(select r.referencetext from k1data.referencemaster r where r.documentid=dm.documentid order by lstupddate desc limit 1) as referencetext,
dm.documentid,
dm.srocode,
dm.registrationdatetime AS executiondate,
dm.cdnumber,
dm.pagecount,
dm.finalregistrationnumber AS documentreference, 
(select decn.note_enteredpart from k1data.dec_drpndnote decn where decn.orderid 
	in (select orderid from k1data.dec_drordermaster d where d.documentid = dm.documentid and d.srocode=dm.srocode order by d.insertdatetime desc limit 1)
	order by insertdatetime desc limit 1) as correctionnote,--Added on 02-01-24 by Shubham, to fetch correction note based on document and not property.
(select string_agg(concat('1. Liability Details: Order Number: ', ld.ordernumber, ', Issue Date: ', TO_CHAR(ld.issuedate ::date, 'dd/mm/yyyy'), 
',Liability Note: ', ld.liabilitynote, '<br>2.  Additional Note: '),';<br> ') as liabilitynote
from k1data.liabilityonpropertydetails lop
join k1data.liabilitydetails ld on lop.liabilityid = ld.liabilityid 
where lop.propertyid = pm.propertyid) as liabilitynote
from k1data.documentmaster dm
join k1data.propertymaster pm on dm.documentid=pm.documentid and dm.srocode=pm.regsrocode and dm.finalregistrationnumber is not null and registrationdatetime is not null
inner join k1data.villagemaster v on pm.villagecode = v.villagecode
inner JOIN k1data.hoblimaster h ON v.hoblicode = h.hoblicode
JOIN k1data.registrationarticles ra ON ra.regarticlecode = dm.regarticlecode
where dm.documentid=_documentid and dm.srocode=_srocode
and dm.bookid not in (3, 4)
and pm.ismovableproperty = false;
-- return v_data_json;
END;
$$;


ALTER FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) OWNER TO postgres;

--
-- Name: fn_fetch_ecjson_prtydtils_k1(bigint, integer); Type: FUNCTION; Schema: k1data; Owner: postgres
--

CREATE FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) RETURNS TABLE(partyid bigint, partyname text, partytypeid integer, address character varying)
    LANGUAGE plpgsql
    AS $$
begin
return query
select distinct p.partyid,
CASE
when p1.partytypeid = 4 AND p2.firstname IS NOT NULL THEN concat(s.descriptione, p.firstname, ' ', p.middlename, ' ', p.lastname, ' is rep. by minor guardian ', s1.descriptione, p1.firstname, ' ', p1.middlename, ' ', p1.lastname, ', whose POA is ', s2.descriptione, p2.firstname, ' ', p2.middlename, ' ', p2.lastname)
WHEN p1.partytypeid = 4 AND p2.firstname IS NULL THEN concat(s.descriptione, p.firstname, ' ', p.middlename, ' ', p.lastname, ' is rep. by minor guardian ', s1.descriptione, p1.firstname, ' ', p1.middlename, ' ', p1.lastname)
WHEN p1.partytypeid = 5 AND p.isorganization = true THEN concat(s.descriptione, p.firstname, ' ', p.middlename, ' ', p.lastname, ' POA by ', s1.descriptione, p1.firstname, ' ', p1.middlename, ' ', p1.lastname, ' is Rep. by ', p1.orgpoaauthsignfname, ' ', p1.orgpoaauthsignlname)
WHEN p1.partytypeid = 5 AND p.isorganization = false THEN concat(s1.descriptione, p1.firstname, ' is POA of ', s.descriptione, p.firstname, ' ', p.middlename, ' ', p.lastname)
WHEN p1.partytypeid = 9 AND p.isorganization = true AND p2.firstname IS NOT NULL THEN concat(s.descriptione, p.firstname, ' ', p.middlename, ' ', p.lastname, ' is Rep. by ', s1.descriptione, p1.firstname, ' ', p1.middlename, ' ', p1.lastname, ', whose POA is ', s2.descriptione, p2.firstname, ' ', p2.middlename, ' ', p2.lastname)
WHEN p1.partytypeid = 9  AND p.isorganization = true AND p2.firstname IS NULL THEN concat(s.descriptione, p.firstname, ' ', p.middlename, ' ', p.lastname, ' is Rep. by ', s1.descriptione, p1.firstname, ' ', p1.middlename, ' ', p1.lastname)
WHEN p1.partytypeid IS NULL AND p.partytypeid = 1 THEN concat(s.descriptione, p.firstname, ' ', p.middlename, ' ', p.lastname)
WHEN p1.partytypeid IS NULL AND p.partytypeid = 2 THEN concat(s.descriptione, p.firstname, ' ', p.middlename, ' ', p.lastname)
ELSE NULL::text
END AS partyname,
p.partytypeid ,
p.address 
from k1data.documentmaster dm 
join k1data.partyinfo p on dm.documentid=p.documentid and dm.srocode=p.srocode
left JOIN k1data.partyinfo p1 ON p.partyid = p1.linkpartyid AND (p1.partytypeid = ANY (ARRAY[9, 4, 5]))
left JOIN k1data.partyinfo p2 ON p2.linkpartyid = p1.partyid AND (p2.partytypeid = ANY (ARRAY[5]))
left JOIN k1data.salutationmaster s ON p.salutationid = s.salutationid
left JOIN k1data.salutationmaster s1 ON p1.salutationid = s1.salutationid
left JOIN k1data.salutationmaster s2 ON p2.salutationid = s2.salutationid
where dm.documentid =_documentid and dm.srocode=_srocode;
--return v_data_json;
END;
$$;


ALTER FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ecnamesearchkeyvaluesk1; Type: TABLE; Schema: k1data; Owner: csgdevdbadmin
--

CREATE TABLE k1data.ecnamesearchkeyvaluesk1 (
    keyid bigint NOT NULL,
    documentid bigint NOT NULL,
    srocode integer NOT NULL,
    partytypeid integer NOT NULL,
    partyid bigint,
    firstname character varying(300) NOT NULL,
    middlename character varying(500),
    lastname character varying(350) NOT NULL,
    orderid bigint,
    isactivated integer DEFAULT 1 NOT NULL,
    actiontype character(1) DEFAULT 'I'::bpchar,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    isudpated boolean DEFAULT false,
    isnotupdate boolean DEFAULT false
);


ALTER TABLE k1data.ecnamesearchkeyvaluesk1 OWNER TO csgdevdbadmin;

--
-- Name: k1dec_drordermaster; Type: TABLE; Schema: k1data; Owner: csgdevdbadmin
--

CREATE TABLE k1data.k1dec_drordermaster (
    orderid bigint NOT NULL,
    districtcode integer,
    srocode integer,
    documentid bigint,
    ordernumber character varying(100),
    orderdate timestamp without time zone,
    isfinalized integer DEFAULT 0,
    userid bigint,
    ipaddress character varying(50),
    insertdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    absolutefilepath character varying(8000),
    relativepath character varying(8000),
    filename character varying(8000),
    isvalid integer DEFAULT 1,
    k1k2_flag smallint DEFAULT 2,
    correctionnote boolean
);


ALTER TABLE k1data.k1dec_drordermaster OWNER TO csgdevdbadmin;

--
-- Name: k1dec_drpndnote; Type: TABLE; Schema: k1data; Owner: csgdevdbadmin
--

CREATE TABLE k1data.k1dec_drpndnote (
    noteid integer NOT NULL,
    orderid bigint NOT NULL,
    propertyid bigint,
    note_preparedpart character varying(4000),
    note_enteredpart character varying(4000),
    userid bigint,
    ipaddress character varying(50),
    insertdatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE k1data.k1dec_drpndnote OWNER TO csgdevdbadmin;

--
-- Name: k1documentmaster; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.k1documentmaster (
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
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE k1data.k1documentmaster OWNER TO postgres;

--
-- Name: k1ecnamesearchkeyvalues; Type: TABLE; Schema: k1data; Owner: csgdevdbadmin
--

CREATE TABLE k1data.k1ecnamesearchkeyvalues (
    keyid bigint NOT NULL,
    documentid bigint NOT NULL,
    srocode integer NOT NULL,
    partytypeid integer NOT NULL,
    partyid bigint,
    firstname character varying(300) NOT NULL,
    middlename character varying(500),
    lastname character varying(350) NOT NULL,
    orderid bigint,
    isactivated integer DEFAULT 1 NOT NULL,
    actiontype character(1) DEFAULT 'I'::bpchar,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE k1data.k1ecnamesearchkeyvalues OWNER TO csgdevdbadmin;

--
-- Name: k1ecpropertysearchkeyvalues; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.k1ecpropertysearchkeyvalues (
    keyid bigint NOT NULL,
    executiondate timestamp without time zone,
    villagecode bigint NOT NULL,
    propertyid bigint NOT NULL,
    regsrocode integer,
    srocode integer NOT NULL,
    documentid bigint NOT NULL,
    newpropertyid bigint,
    newregsrocode integer,
    newsrocode integer,
    currentpropertytypeid integer NOT NULL,
    currentnumber character varying(1000) NOT NULL,
    oldpropertytypeid integer,
    oldnumber character varying(1000),
    survey_no integer,
    surnoc character varying(1000),
    hissa_no character varying(1000),
    orderid bigint,
    isactivated integer DEFAULT 1 NOT NULL,
    actiontype character(1) DEFAULT 'I'::bpchar,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2
);


ALTER TABLE k1data.k1ecpropertysearchkeyvalues OWNER TO postgres;

--
-- Name: k1partyinfo_partyid_seq; Type: SEQUENCE; Schema: k1data; Owner: postgres
--

CREATE SEQUENCE k1data.k1partyinfo_partyid_seq
    START WITH 7906329
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 922337203767
    CACHE 1;


ALTER TABLE k1data.k1partyinfo_partyid_seq OWNER TO postgres;

--
-- Name: k1partyinfo; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.k1partyinfo (
    partyid bigint DEFAULT nextval('k1data.k1partyinfo_partyid_seq'::regclass) NOT NULL,
    srocode integer NOT NULL,
    documentid bigint NOT NULL,
    partytypeid integer NOT NULL,
    firstname character varying(1000),
    middlename character varying(1000),
    lastname character varying(1000),
    address character varying(1000) NOT NULL,
    age character varying(1000),
    sex smallint,
    isexecutor boolean NOT NULL,
    ispresenter boolean NOT NULL,
    admissiondate timestamp without time zone,
    aliasname character varying(300),
    correctedname character varying(300),
    relationship character varying(1000),
    relativename character varying(1000),
    epic character varying(1000),
    pan character varying(1000),
    phonenumber character varying(100),
    availableextacre integer,
    availableextgunta integer,
    availableextfgunta numeric(8,5),
    bincom character varying(1000),
    category character varying(1000),
    dateofdeath timestamp without time zone,
    fingerid integer,
    fingerverificationstatusid smallint,
    ispartofrtc boolean,
    landcode bigint,
    mainownerno bigint,
    ownerno bigint,
    partypoa character varying(2000),
    photopath character varying(2000),
    poaadmission bigint,
    poapresentation bigint,
    primaryseller boolean,
    profession character varying(2000),
    restriction character varying(1000),
    restrictiondescription character varying(2000),
    restrictiontype character varying(500),
    section88exemption boolean,
    thumbmatchfailedreasonid integer,
    thumbminutiae bytea,
    thumbpath character varying(1000),
    totalextacre integer,
    totalextgunta integer,
    totalextfgunta numeric(8,5),
    transactextacre integer,
    transactextgunta integer,
    transactextfgunta numeric(8,5),
    volumename character varying(2000),
    hasgpa boolean,
    isaua boolean,
    importedpartyparentid bigint,
    salutationid smallint,
    isorganization boolean DEFAULT false,
    organizationid integer,
    applicationnumber character varying(1000),
    verified boolean DEFAULT false,
    issroapproved character varying(500) DEFAULT 'E'::character varying,
    districtcode integer,
    talukcode integer,
    hoblicode integer,
    villagecode bigint,
    tanno character varying(2000),
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
    isendorseprinted boolean DEFAULT false,
    thumbremarks character varying(1000),
    partyidreference bigint,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    ispartyrefused boolean DEFAULT false,
    age_k1 character varying(2000),
    isupdated boolean DEFAULT false,
    isudpated boolean DEFAULT false,
    isreverted boolean DEFAULT false
);


ALTER TABLE k1data.k1partyinfo OWNER TO postgres;

--
-- Name: k1partyinfo_updatetest; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.k1partyinfo_updatetest (
    partyid bigint,
    srocode integer,
    documentid bigint,
    partytypeid integer,
    firstname character varying(1000),
    middlename character varying(1000),
    lastname character varying(1000),
    address character varying(1000),
    age character varying(1000),
    sex smallint,
    isexecutor boolean,
    ispresenter boolean,
    admissiondate timestamp without time zone,
    aliasname character varying(300),
    correctedname character varying(300),
    relationship character varying(1000),
    relativename character varying(1000),
    epic character varying(1000),
    pan character varying(1000),
    phonenumber character varying(100),
    availableextacre integer,
    availableextgunta integer,
    availableextfgunta numeric(8,5),
    bincom character varying(1000),
    category character varying(1000),
    dateofdeath timestamp without time zone,
    fingerid integer,
    fingerverificationstatusid smallint,
    ispartofrtc boolean,
    landcode bigint,
    mainownerno bigint,
    ownerno bigint,
    partypoa character varying(2000),
    photopath character varying(2000),
    poaadmission bigint,
    poapresentation bigint,
    primaryseller boolean,
    profession character varying(2000),
    restriction character varying(1000),
    restrictiondescription character varying(2000),
    restrictiontype character varying(500),
    section88exemption boolean,
    thumbmatchfailedreasonid integer,
    thumbminutiae bytea,
    thumbpath character varying(1000),
    totalextacre integer,
    totalextgunta integer,
    totalextfgunta numeric(8,5),
    transactextacre integer,
    transactextgunta integer,
    transactextfgunta numeric(8,5),
    volumename character varying(2000),
    hasgpa boolean,
    isaua boolean,
    importedpartyparentid bigint,
    salutationid smallint,
    isorganization boolean,
    organizationid integer,
    applicationnumber character varying(1000),
    verified boolean,
    issroapproved character varying(500),
    districtcode integer,
    talukcode integer,
    hoblicode integer,
    villagecode bigint,
    tanno character varying(2000),
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
    thumbremarks character varying(1000),
    partyidreference bigint,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    ispartyrefused boolean,
    age_k1 character varying(2000),
    isupdated boolean,
    surid bigint NOT NULL
);


ALTER TABLE k1data.k1partyinfo_updatetest OWNER TO postgres;

--
-- Name: k1partyinfo_updatetest_surid_seq; Type: SEQUENCE; Schema: k1data; Owner: postgres
--

CREATE SEQUENCE k1data.k1partyinfo_updatetest_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE k1data.k1partyinfo_updatetest_surid_seq OWNER TO postgres;

--
-- Name: k1partyinfo_updatetest_surid_seq; Type: SEQUENCE OWNED BY; Schema: k1data; Owner: postgres
--

ALTER SEQUENCE k1data.k1partyinfo_updatetest_surid_seq OWNED BY k1data.k1partyinfo_updatetest.surid;


--
-- Name: k1propertymaster; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.k1propertymaster (
    propertyid bigint NOT NULL,
    documentid bigint NOT NULL,
    villagecode bigint,
    regsrocode integer NOT NULL,
    srocode integer NOT NULL,
    totalarea numeric(18,4) NOT NULL,
    unitid integer NOT NULL,
    northboundary character varying(1000),
    southboundary character varying(1000),
    eastboundary character varying(1000),
    westboundary character varying(1000),
    landmark character varying(5000),
    marketvalue numeric,
    assessment character varying(2000),
    sdcalculationstring character varying(1000),
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
    restriction character varying(500),
    restrictiontype character varying(500),
    restrictiondescription character varying(500),
    enumber character varying(20),
    claimingblocknumber character varying(500),
    retainingblocknumber character varying(500),
    valuationreport character varying(4000),
    loanpurposeid smallint,
    applicationnumber character varying(50),
    verified boolean DEFAULT false,
    issroapproved character varying(500) DEFAULT 'E'::character varying,
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
    sronoofscanpages integer DEFAULT 0,
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
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    zoneid integer,
    subpropertytypeid integer,
    k1k2_flag smallint DEFAULT 2,
    "11ENumber" character varying,
    isudpated boolean DEFAULT false
);


ALTER TABLE k1data.k1propertymaster OWNER TO postgres;

--
-- Name: k1propertynumberdetails; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.k1propertynumberdetails (
    propertyid bigint NOT NULL,
    srocode integer NOT NULL,
    currentpropertytypeid integer NOT NULL,
    currentnumber character varying(1000) NOT NULL,
    oldpropertytypeid integer,
    oldnumber character varying(500),
    description character varying(1000),
    survey_no integer,
    surnoc character varying(1000),
    hissa_no character varying(500),
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    isudpated boolean DEFAULT false
);


ALTER TABLE k1data.k1propertynumberdetails OWNER TO postgres;

--
-- Name: k1propertynumberdetails_new1; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.k1propertynumberdetails_new1 (
    propertyid bigint,
    srocode integer,
    currentpropertytypeid integer,
    currentnumber character varying(1000),
    oldpropertytypeid integer,
    oldnumber character varying(500),
    description character varying(1000),
    survey_no integer,
    surnoc character varying(1000),
    hissa_no character varying(500),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    isudpated boolean,
    surid bigint NOT NULL
);


ALTER TABLE k1data.k1propertynumberdetails_new1 OWNER TO postgres;

--
-- Name: k1propertynumberdetails_new1_surid_seq; Type: SEQUENCE; Schema: k1data; Owner: postgres
--

CREATE SEQUENCE k1data.k1propertynumberdetails_new1_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE k1data.k1propertynumberdetails_new1_surid_seq OWNER TO postgres;

--
-- Name: k1propertynumberdetails_new1_surid_seq; Type: SEQUENCE OWNED BY; Schema: k1data; Owner: postgres
--

ALTER SEQUENCE k1data.k1propertynumberdetails_new1_surid_seq OWNED BY k1data.k1propertynumberdetails_new1.surid;


--
-- Name: k1propertyschedules; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.k1propertyschedules (
    scheduleid bigint NOT NULL,
    propertyid bigint NOT NULL,
    srocode integer NOT NULL,
    partyid bigint,
    scheduletype character varying(100),
    totalarea numeric(18,4) NOT NULL,
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
    k1k2_flag smallint DEFAULT 2,
    isudpated boolean DEFAULT false,
    isreverted boolean DEFAULT false,
    surid bigint NOT NULL
);


ALTER TABLE k1data.k1propertyschedules OWNER TO postgres;

--
-- Name: k1propertyschedules_new_1; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.k1propertyschedules_new_1 (
    scheduleid bigint,
    propertyid bigint,
    srocode integer,
    partyid bigint,
    scheduletype character varying(100),
    totalarea numeric(18,4),
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
    isudpated boolean,
    isreverted boolean,
    surid bigint NOT NULL
);


ALTER TABLE k1data.k1propertyschedules_new_1 OWNER TO postgres;

--
-- Name: k1propertyschedules_new_1_surid_seq; Type: SEQUENCE; Schema: k1data; Owner: postgres
--

CREATE SEQUENCE k1data.k1propertyschedules_new_1_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE k1data.k1propertyschedules_new_1_surid_seq OWNER TO postgres;

--
-- Name: k1propertyschedules_new_1_surid_seq; Type: SEQUENCE OWNED BY; Schema: k1data; Owner: postgres
--

ALTER SEQUENCE k1data.k1propertyschedules_new_1_surid_seq OWNED BY k1data.k1propertyschedules_new_1.surid;


--
-- Name: k1propertyschedules_surid_seq; Type: SEQUENCE; Schema: k1data; Owner: postgres
--

CREATE SEQUENCE k1data.k1propertyschedules_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE k1data.k1propertyschedules_surid_seq OWNER TO postgres;

--
-- Name: k1propertyschedules_surid_seq; Type: SEQUENCE OWNED BY; Schema: k1data; Owner: postgres
--

ALTER SEQUENCE k1data.k1propertyschedules_surid_seq OWNED BY k1data.k1propertyschedules.surid;


--
-- Name: propertymaster_new2; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.propertymaster_new2 (
    propertyid bigint,
    documentid bigint,
    villagecode bigint,
    regsrocode integer,
    srocode integer,
    totalarea numeric(18,4),
    unitid integer,
    northboundary character varying(1000),
    southboundary character varying(1000),
    eastboundary character varying(1000),
    westboundary character varying(1000),
    landmark character varying(5000),
    marketvalue numeric,
    assessment character varying(2000),
    sdcalculationstring character varying(1000),
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
    restriction character varying(500),
    restrictiontype character varying(500),
    restrictiondescription character varying(500),
    enumber character varying(20),
    claimingblocknumber character varying(500),
    retainingblocknumber character varying(500),
    valuationreport character varying(4000),
    loanpurposeid smallint,
    applicationnumber character varying(50),
    verified boolean,
    issroapproved character varying(500),
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
    "11ENumber" character varying,
    isudpated boolean,
    surid bigint NOT NULL
);


ALTER TABLE k1data.propertymaster_new2 OWNER TO postgres;

--
-- Name: propertymaster_new2_surid_seq; Type: SEQUENCE; Schema: k1data; Owner: postgres
--

CREATE SEQUENCE k1data.propertymaster_new2_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE k1data.propertymaster_new2_surid_seq OWNER TO postgres;

--
-- Name: propertymaster_new2_surid_seq; Type: SEQUENCE OWNED BY; Schema: k1data; Owner: postgres
--

ALTER SEQUENCE k1data.propertymaster_new2_surid_seq OWNED BY k1data.propertymaster_new2.surid;


--
-- Name: villagemastervillagesmergingmappping; Type: TABLE; Schema: k1data; Owner: postgres
--

CREATE TABLE k1data.villagemastervillagesmergingmappping (
    id bigint,
    srocode bigint,
    villagecode bigint,
    mergedvillagecode bigint,
    surid bigint NOT NULL
);


ALTER TABLE k1data.villagemastervillagesmergingmappping OWNER TO postgres;

--
-- Name: villagemastervillagesmergingmappping_surid_seq; Type: SEQUENCE; Schema: k1data; Owner: postgres
--

CREATE SEQUENCE k1data.villagemastervillagesmergingmappping_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE k1data.villagemastervillagesmergingmappping_surid_seq OWNER TO postgres;

--
-- Name: villagemastervillagesmergingmappping_surid_seq; Type: SEQUENCE OWNED BY; Schema: k1data; Owner: postgres
--

ALTER SEQUENCE k1data.villagemastervillagesmergingmappping_surid_seq OWNED BY k1data.villagemastervillagesmergingmappping.surid;


--
-- Name: k1partyinfo_updatetest surid; Type: DEFAULT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1partyinfo_updatetest ALTER COLUMN surid SET DEFAULT nextval('k1data.k1partyinfo_updatetest_surid_seq'::regclass);


--
-- Name: k1propertynumberdetails_new1 surid; Type: DEFAULT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1propertynumberdetails_new1 ALTER COLUMN surid SET DEFAULT nextval('k1data.k1propertynumberdetails_new1_surid_seq'::regclass);


--
-- Name: k1propertyschedules surid; Type: DEFAULT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1propertyschedules ALTER COLUMN surid SET DEFAULT nextval('k1data.k1propertyschedules_surid_seq'::regclass);


--
-- Name: k1propertyschedules_new_1 surid; Type: DEFAULT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1propertyschedules_new_1 ALTER COLUMN surid SET DEFAULT nextval('k1data.k1propertyschedules_new_1_surid_seq'::regclass);


--
-- Name: propertymaster_new2 surid; Type: DEFAULT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.propertymaster_new2 ALTER COLUMN surid SET DEFAULT nextval('k1data.propertymaster_new2_surid_seq'::regclass);


--
-- Name: villagemastervillagesmergingmappping surid; Type: DEFAULT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.villagemastervillagesmergingmappping ALTER COLUMN surid SET DEFAULT nextval('k1data.villagemastervillagesmergingmappping_surid_seq'::regclass);


--
-- Name: k1partyinfo_updatetest k1partyinfo_updatetest_pkey; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1partyinfo_updatetest
    ADD CONSTRAINT k1partyinfo_updatetest_pkey PRIMARY KEY (surid);


--
-- Name: k1propertynumberdetails_new1 k1propertynumberdetails_new1_pkey; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1propertynumberdetails_new1
    ADD CONSTRAINT k1propertynumberdetails_new1_pkey PRIMARY KEY (surid);


--
-- Name: k1propertyschedules_new_1 k1propertyschedules_new_1_pkey; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1propertyschedules_new_1
    ADD CONSTRAINT k1propertyschedules_new_1_pkey PRIMARY KEY (surid);


--
-- Name: k1propertyschedules k1propertyschedules_pkey; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1propertyschedules
    ADD CONSTRAINT k1propertyschedules_pkey PRIMARY KEY (surid);


--
-- Name: k1dec_drordermaster pk_dec_drordermaster; Type: CONSTRAINT; Schema: k1data; Owner: csgdevdbadmin
--

ALTER TABLE ONLY k1data.k1dec_drordermaster
    ADD CONSTRAINT pk_dec_drordermaster PRIMARY KEY (orderid);


--
-- Name: k1dec_drpndnote pk_dec_pndnote; Type: CONSTRAINT; Schema: k1data; Owner: csgdevdbadmin
--

ALTER TABLE ONLY k1data.k1dec_drpndnote
    ADD CONSTRAINT pk_dec_pndnote PRIMARY KEY (noteid);


--
-- Name: k1ecnamesearchkeyvalues pk_ecnamesearchkeyvalues; Type: CONSTRAINT; Schema: k1data; Owner: csgdevdbadmin
--

ALTER TABLE ONLY k1data.k1ecnamesearchkeyvalues
    ADD CONSTRAINT pk_ecnamesearchkeyvalues PRIMARY KEY (keyid);


--
-- Name: ecnamesearchkeyvaluesk1 pk_ecnamesearchkeyvalues_keyid; Type: CONSTRAINT; Schema: k1data; Owner: csgdevdbadmin
--

ALTER TABLE ONLY k1data.ecnamesearchkeyvaluesk1
    ADD CONSTRAINT pk_ecnamesearchkeyvalues_keyid PRIMARY KEY (keyid);


--
-- Name: k1ecpropertysearchkeyvalues pk_ecpropertysearchkeyvalues; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1ecpropertysearchkeyvalues
    ADD CONSTRAINT pk_ecpropertysearchkeyvalues PRIMARY KEY (keyid);


--
-- Name: k1documentmaster pk_k1documentmaster_docid_srocode; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1documentmaster
    ADD CONSTRAINT pk_k1documentmaster_docid_srocode PRIMARY KEY (documentid, srocode);


--
-- Name: k1partyinfo pk_k1partyinfo_party_sro; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1partyinfo
    ADD CONSTRAINT pk_k1partyinfo_party_sro PRIMARY KEY (partyid, srocode);


--
-- Name: k1propertynumberdetails pk_pro_sro_current; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1propertynumberdetails
    ADD CONSTRAINT pk_pro_sro_current PRIMARY KEY (propertyid, srocode, currentpropertytypeid);


--
-- Name: propertymaster_new2 propertymaster_new2_pkey; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.propertymaster_new2
    ADD CONSTRAINT propertymaster_new2_pkey PRIMARY KEY (surid);


--
-- Name: k1propertymaster propertymaster_pkey; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.k1propertymaster
    ADD CONSTRAINT propertymaster_pkey PRIMARY KEY (propertyid, regsrocode);


--
-- Name: villagemastervillagesmergingmappping villagemastervillagesmergingmappping_pkey; Type: CONSTRAINT; Schema: k1data; Owner: postgres
--

ALTER TABLE ONLY k1data.villagemastervillagesmergingmappping
    ADD CONSTRAINT villagemastervillagesmergingmappping_pkey PRIMARY KEY (surid);


--
-- Name: documentmaster_bookid_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX documentmaster_bookid_idx_k1 ON k1data.k1documentmaster USING btree (bookid);


--
-- Name: documentmaster_multiple_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE UNIQUE INDEX documentmaster_multiple_k1 ON k1data.k1documentmaster USING btree (applicationnumber);


--
-- Name: documentmaster_regarticlecode_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX documentmaster_regarticlecode_idx_k1 ON k1data.k1documentmaster USING btree (regarticlecode);


--
-- Name: documentmaster_registrationdatetime_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX documentmaster_registrationdatetime_idx_k1 ON k1data.k1documentmaster USING btree (registrationdatetime);


--
-- Name: ecpropertysearchkeyvalues_docid_idx; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX ecpropertysearchkeyvalues_docid_idx ON k1data.k1ecpropertysearchkeyvalues USING btree (propertyid, documentid);


--
-- Name: fki_fk_propertynumberdetails_propertynotypemaster; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX fki_fk_propertynumberdetails_propertynotypemaster ON k1data.k1propertynumberdetails USING btree (currentpropertytypeid);


--
-- Name: fki_fk_propertynumberdetails_propertynotypemaster_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX fki_fk_propertynumberdetails_propertynotypemaster_k1 ON k1data.k1propertynumberdetails USING btree (currentpropertytypeid);


--
-- Name: idx_currentnumber; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_currentnumber ON k1data.k1ecpropertysearchkeyvalues USING btree (currentnumber, currentpropertytypeid);


--
-- Name: idx_currentnumber_property; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_currentnumber_property ON k1data.k1propertynumberdetails USING btree (currentpropertytypeid, currentnumber);


--
-- Name: idx_currentnumber_property_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_currentnumber_property_k1 ON k1data.k1propertynumberdetails USING btree (currentpropertytypeid, currentnumber);


--
-- Name: idx_decdromasterdocidsrocode; Type: INDEX; Schema: k1data; Owner: csgdevdbadmin
--

CREATE INDEX idx_decdromasterdocidsrocode ON k1data.k1dec_drordermaster USING btree (documentid, srocode);


--
-- Name: idx_decdromasterfinalized; Type: INDEX; Schema: k1data; Owner: csgdevdbadmin
--

CREATE INDEX idx_decdromasterfinalized ON k1data.k1dec_drordermaster USING btree (isfinalized);


--
-- Name: idx_documentmaster_final_rega_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_documentmaster_final_rega_k1 ON k1data.k1documentmaster USING btree (finalregistrationnumber, regarticlecode);


--
-- Name: idx_ecpropertysearchkeyvaluesdocid; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_ecpropertysearchkeyvaluesdocid ON k1data.k1ecpropertysearchkeyvalues USING btree (documentid);


--
-- Name: idx_isudpated_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_isudpated_k1 ON k1data.k1partyinfo USING btree (isudpated);


--
-- Name: idx_k1documentmaster_document_sro; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_k1documentmaster_document_sro ON k1data.k1documentmaster USING btree (documentid, srocode);


--
-- Name: idx_k1ecpropertysearchkeyvalues_propertyid; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_k1ecpropertysearchkeyvalues_propertyid ON k1data.k1ecpropertysearchkeyvalues USING btree (propertyid);


--
-- Name: idx_k1ecpropertysearchkeyvalues_regsrocode; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_k1ecpropertysearchkeyvalues_regsrocode ON k1data.k1ecpropertysearchkeyvalues USING btree (regsrocode);


--
-- Name: idx_k1ecpropertysearchkeyvalues_srocode; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_k1ecpropertysearchkeyvalues_srocode ON k1data.k1ecpropertysearchkeyvalues USING btree (srocode);


--
-- Name: idx_namesearchsrocode; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_namesearchsrocode ON k1data.k1ecpropertysearchkeyvalues USING btree (srocode);


--
-- Name: idx_partyid_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_partyid_k1 ON k1data.k1partyinfo USING btree (partyid);


--
-- Name: idx_partyinfo_districtcode_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_partyinfo_districtcode_k1 ON k1data.k1partyinfo USING btree (districtcode);


--
-- Name: idx_partyinfo_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_partyinfo_k1 ON k1data.k1partyinfo USING btree (applicationnumber);


--
-- Name: idx_partyinfo_linkedpartyid_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_partyinfo_linkedpartyid_k1 ON k1data.k1partyinfo USING btree (linkpartyid);


--
-- Name: idx_partyinfo_propertyids_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_partyinfo_propertyids_k1 ON k1data.k1partyinfo USING btree (propertyid);


--
-- Name: idx_pm_documentid_regsro; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_pm_documentid_regsro ON k1data.k1propertymaster USING btree (documentid, regsrocode);


--
-- Name: idx_proeprtymasterappno; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_proeprtymasterappno ON k1data.k1propertymaster USING btree (documentid);


--
-- Name: idx_proeprtymastersrocode; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_proeprtymastersrocode ON k1data.k1propertymaster USING btree (srocode);


--
-- Name: idx_propertymaster_road_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_propertymaster_road_1 ON k1data.k1propertymaster USING btree (roadcode);


--
-- Name: idx_propertymaster_stamp_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_propertymaster_stamp_1 ON k1data.k1propertymaster USING btree (stamparticlecode);


--
-- Name: idx_propertyschedules_propertyid_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_propertyschedules_propertyid_k1 ON k1data.k1propertyschedules USING btree (propertyid);


--
-- Name: idx_propertyschedules_propertyids_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_propertyschedules_propertyids_k1 ON k1data.k1propertyschedules USING btree (applicationnumber);


--
-- Name: idx_ps_propertyid_srocode; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_ps_propertyid_srocode ON k1data.k1propertyschedules USING btree (propertyid, srocode);


--
-- Name: idx_villagecodemerged; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX idx_villagecodemerged ON k1data.villagemastervillagesmergingmappping USING btree (villagecode);


--
-- Name: ix_nc_finalregnumber_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX ix_nc_finalregnumber_k1 ON k1data.k1documentmaster USING btree (finalregistrationnumber);


--
-- Name: ix_partyinfo_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE UNIQUE INDEX ix_partyinfo_k1 ON k1data.k1partyinfo USING btree (srocode, documentid, partyid) INCLUDE (partytypeid, firstname, middlename, lastname, address);


--
-- Name: ix_propertymaster_1_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX ix_propertymaster_1_1 ON k1data.k1propertymaster USING btree (villagecode, ismovableproperty) INCLUDE (propertyid, documentid, regsrocode, srocode);


--
-- Name: ix_propertymaster_4_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX ix_propertymaster_4_1 ON k1data.k1propertymaster USING btree (applicationnumber DESC NULLS LAST);


--
-- Name: ix_propertymaster_appl_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX ix_propertymaster_appl_1 ON k1data.k1propertymaster USING btree (applicationnumber DESC);


--
-- Name: partyinfo_documentid_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX partyinfo_documentid_idx_k1 ON k1data.k1partyinfo USING btree (documentid);


--
-- Name: partyinfo_multiple_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX partyinfo_multiple_k1 ON k1data.k1partyinfo USING btree (partytypeid, applicationnumber, linkpartyid);


--
-- Name: partyinfo_srocode_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX partyinfo_srocode_idx_k1 ON k1data.k1partyinfo USING btree (srocode);


--
-- Name: propertymaster_ismovableproperty_idx_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX propertymaster_ismovableproperty_idx_1 ON k1data.k1propertymaster USING btree (ismovableproperty);


--
-- Name: propertymaster_multiple_3_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX propertymaster_multiple_3_1 ON k1data.k1propertymaster USING btree (propertyid, applicationnumber, propertytypeid, srocode, villagecode);


--
-- Name: propertymaster_unitid_idx_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX propertymaster_unitid_idx_1 ON k1data.k1propertymaster USING btree (unitid);


--
-- Name: propertymaster_villagecode_idx_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX propertymaster_villagecode_idx_1 ON k1data.k1propertymaster USING btree (villagecode);


--
-- Name: propertynumberdetails_currentpropertytypeid_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX propertynumberdetails_currentpropertytypeid_idx_k1 ON k1data.k1propertynumberdetails USING btree (currentpropertytypeid);


--
-- Name: propertynumberdetails_propertyid_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX propertynumberdetails_propertyid_idx_k1 ON k1data.k1propertynumberdetails USING btree (propertyid);


--
-- Name: propertynumberdetails_srocode_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX propertynumberdetails_srocode_idx_k1 ON k1data.k1propertynumberdetails USING btree (srocode);


--
-- Name: propertyschedules_scheduleid_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX propertyschedules_scheduleid_idx_k1 ON k1data.k1propertyschedules USING btree (scheduleid);


--
-- Name: propertyschedules_srocode_idx_k1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX propertyschedules_srocode_idx_k1 ON k1data.k1propertyschedules USING btree (srocode);


--
-- Name: scheduleid_regsrocode_idx_1; Type: INDEX; Schema: k1data; Owner: postgres
--

CREATE INDEX scheduleid_regsrocode_idx_1 ON k1data.k1propertymaster USING btree (stampruleid);


--
-- Name: k1ecnamesearchkeyvalues fk_ecnamesearchkeyvalues_dec_drordermaster1; Type: FK CONSTRAINT; Schema: k1data; Owner: csgdevdbadmin
--

ALTER TABLE ONLY k1data.k1ecnamesearchkeyvalues
    ADD CONSTRAINT fk_ecnamesearchkeyvalues_dec_drordermaster1 FOREIGN KEY (orderid) REFERENCES k1data.k1dec_drordermaster(orderid) ON DELETE CASCADE;


--
-- Name: ecnamesearchkeyvaluesk1 fk_ecnamesearchkeyvalues_dec_drordermaster1; Type: FK CONSTRAINT; Schema: k1data; Owner: csgdevdbadmin
--

ALTER TABLE ONLY k1data.ecnamesearchkeyvaluesk1
    ADD CONSTRAINT fk_ecnamesearchkeyvalues_dec_drordermaster1 FOREIGN KEY (orderid) REFERENCES k1data.k1dec_drordermaster(orderid) ON DELETE CASCADE;


--
-- Name: SCHEMA k1data; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA k1data TO csgadmin;
GRANT USAGE ON SCHEMA k1data TO csgcitizenuser;
GRANT USAGE ON SCHEMA k1data TO csgdeptuser;
GRANT USAGE ON SCHEMA k1data TO bkpuser;
GRANT USAGE ON SCHEMA k1data TO jslip_user;
GRANT USAGE ON SCHEMA k1data TO ramachandrak;
GRANT USAGE ON SCHEMA k1data TO csgk2user;
GRANT USAGE ON SCHEMA k1data TO pavitra;
GRANT USAGE ON SCHEMA k1data TO abhijeet;
GRANT USAGE ON SCHEMA k1data TO test_user;
GRANT USAGE ON SCHEMA k1data TO sshuser;
GRANT USAGE ON SCHEMA k1data TO shrikanth;
GRANT USAGE ON SCHEMA k1data TO venkat;
GRANT USAGE ON SCHEMA k1data TO chethanahana;
GRANT USAGE ON SCHEMA k1data TO sachinahana;


--
-- Name: TYPE k1ec_srch_property; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT ALL ON TYPE k1data.k1ec_srch_property TO csgcitizenuser;
GRANT ALL ON TYPE k1data.k1ec_srch_property TO csgdeptuser;
GRANT ALL ON TYPE k1data.k1ec_srch_property TO csgk2user;
GRANT ALL ON TYPE k1data.k1ec_srch_property TO csgkaverirwx;
GRANT ALL ON TYPE k1data.k1ec_srch_property TO jslip;
GRANT ALL ON TYPE k1data.k1ec_srch_property TO raghavendra;
GRANT ALL ON TYPE k1data.k1ec_srch_property TO sumit WITH GRANT OPTION;
GRANT ALL ON TYPE k1data.k1ec_srch_property TO test_user;


--
-- Name: FUNCTION fn_ec_prptysch_k1(_propertyid bigint, _srocode integer); Type: ACL; Schema: k1data; Owner: postgres
--

GRANT ALL ON FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) TO csgadmin;
GRANT ALL ON FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) TO csgcitizenuser;
GRANT ALL ON FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) TO csgdeptuser;
GRANT ALL ON FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) TO csgk2user;
GRANT ALL ON FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) TO csgkaverirwx;
GRANT ALL ON FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) TO jslip;
GRANT ALL ON FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) TO raghavendra;
GRANT ALL ON FUNCTION k1data.fn_ec_prptysch_k1(_propertyid bigint, _srocode integer) TO test_user;


--
-- Name: FUNCTION fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone); Type: ACL; Schema: k1data; Owner: postgres
--

GRANT ALL ON FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) TO csgadmin;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) TO csgcitizenuser;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) TO csgdeptuser;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) TO csgk2user;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) TO csgkaverirwx;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) TO jslip;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) TO raghavendra;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecdocid_k1(_villagecode integer, p_srch_property k1data.k1ec_srch_property[], _fromdate timestamp without time zone, _todate timestamp without time zone) TO test_user;


--
-- Name: FUNCTION fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint); Type: ACL; Schema: k1data; Owner: postgres
--

GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) TO csgadmin;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) TO csgcitizenuser;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) TO csgdeptuser;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) TO csgk2user;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) TO csgkaverirwx;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) TO jslip;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) TO raghavendra;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_chk_docdetails_k1(_documentid bigint, _srocode bigint) TO test_user;


--
-- Name: FUNCTION fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer); Type: ACL; Schema: k1data; Owner: postgres
--

GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) TO sumit WITH GRANT OPTION;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) TO csgadmin;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) TO csgcitizenuser;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) TO csgdeptuser;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) TO csgk2user;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) TO csgkaverirwx;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) TO jslip;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) TO raghavendra;
GRANT ALL ON FUNCTION k1data.fn_fetch_ecjson_prtydtils_k1(_documentid bigint, _srocode integer) TO test_user;


--
-- Name: TABLE ecnamesearchkeyvaluesk1; Type: ACL; Schema: k1data; Owner: csgdevdbadmin
--

REVOKE ALL ON TABLE k1data.ecnamesearchkeyvaluesk1 FROM csgdevdbadmin;
GRANT SELECT,REFERENCES ON TABLE k1data.ecnamesearchkeyvaluesk1 TO csgk2user;
GRANT SELECT ON TABLE k1data.ecnamesearchkeyvaluesk1 TO ramachandrak;
GRANT ALL ON TABLE k1data.ecnamesearchkeyvaluesk1 TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE k1data.ecnamesearchkeyvaluesk1 TO pavitra;
GRANT SELECT ON TABLE k1data.ecnamesearchkeyvaluesk1 TO deptdba;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.ecnamesearchkeyvaluesk1 TO abhijeet;
GRANT SELECT,REFERENCES ON TABLE k1data.ecnamesearchkeyvaluesk1 TO test_user;
GRANT SELECT,REFERENCES ON TABLE k1data.ecnamesearchkeyvaluesk1 TO sshuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.ecnamesearchkeyvaluesk1 TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.ecnamesearchkeyvaluesk1 TO csgdeptuser;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.ecnamesearchkeyvaluesk1 TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.ecnamesearchkeyvaluesk1 TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.ecnamesearchkeyvaluesk1 TO sachinahana;


--
-- Name: TABLE k1dec_drordermaster; Type: ACL; Schema: k1data; Owner: csgdevdbadmin
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1dec_drordermaster TO csgk2user;
GRANT SELECT ON TABLE k1data.k1dec_drordermaster TO ramachandrak;
GRANT ALL ON TABLE k1data.k1dec_drordermaster TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE k1data.k1dec_drordermaster TO pavitra;
GRANT SELECT ON TABLE k1data.k1dec_drordermaster TO deptdba;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drordermaster TO abhijeet;
GRANT SELECT,REFERENCES ON TABLE k1data.k1dec_drordermaster TO test_user;
GRANT SELECT,REFERENCES ON TABLE k1data.k1dec_drordermaster TO sshuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drordermaster TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drordermaster TO csgdeptuser;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drordermaster TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drordermaster TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drordermaster TO sachinahana;


--
-- Name: TABLE k1dec_drpndnote; Type: ACL; Schema: k1data; Owner: csgdevdbadmin
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1dec_drpndnote TO csgk2user;
GRANT SELECT ON TABLE k1data.k1dec_drpndnote TO ramachandrak;
GRANT ALL ON TABLE k1data.k1dec_drpndnote TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE k1data.k1dec_drpndnote TO pavitra;
GRANT SELECT ON TABLE k1data.k1dec_drpndnote TO deptdba;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drpndnote TO abhijeet;
GRANT SELECT,REFERENCES ON TABLE k1data.k1dec_drpndnote TO test_user;
GRANT SELECT,REFERENCES ON TABLE k1data.k1dec_drpndnote TO sshuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drpndnote TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drpndnote TO csgdeptuser;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drpndnote TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drpndnote TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1dec_drpndnote TO sachinahana;


--
-- Name: TABLE k1documentmaster; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1documentmaster TO csgk2user;
GRANT ALL ON TABLE k1data.k1documentmaster TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE k1data.k1documentmaster TO csgadmin;
GRANT ALL ON TABLE k1data.k1documentmaster TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1documentmaster TO csgdeptuser;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE k1data.k1documentmaster TO csgkaverirwx;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE k1data.k1documentmaster TO csgmig;
GRANT ALL ON TABLE k1data.k1documentmaster TO csgreplica;
GRANT SELECT,REFERENCES ON TABLE k1data.k1documentmaster TO csgusermis;
GRANT SELECT,REFERENCES ON TABLE k1data.k1documentmaster TO jslip;
GRANT ALL ON TABLE k1data.k1documentmaster TO malathi_s;
GRANT ALL ON TABLE k1data.k1documentmaster TO raghavendra;
GRANT SELECT,REFERENCES ON TABLE k1data.k1documentmaster TO sshuser;
GRANT ALL ON TABLE k1data.k1documentmaster TO test_user;
GRANT ALL ON TABLE k1data.k1documentmaster TO vijaylakshmi;
GRANT SELECT ON TABLE k1data.k1documentmaster TO ramachandrak;
GRANT SELECT ON TABLE k1data.k1documentmaster TO pavitra;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1documentmaster TO abhijeet;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1documentmaster TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1documentmaster TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1documentmaster TO sachinahana;


--
-- Name: TABLE k1ecnamesearchkeyvalues; Type: ACL; Schema: k1data; Owner: csgdevdbadmin
--

REVOKE ALL ON TABLE k1data.k1ecnamesearchkeyvalues FROM csgdevdbadmin;
GRANT SELECT,REFERENCES ON TABLE k1data.k1ecnamesearchkeyvalues TO csgk2user;
GRANT SELECT ON TABLE k1data.k1ecnamesearchkeyvalues TO ramachandrak;
GRANT ALL ON TABLE k1data.k1ecnamesearchkeyvalues TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE k1data.k1ecnamesearchkeyvalues TO pavitra;
GRANT SELECT ON TABLE k1data.k1ecnamesearchkeyvalues TO deptdba;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1ecnamesearchkeyvalues TO abhijeet;
GRANT SELECT,REFERENCES ON TABLE k1data.k1ecnamesearchkeyvalues TO test_user;
GRANT SELECT,REFERENCES ON TABLE k1data.k1ecnamesearchkeyvalues TO sshuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1ecnamesearchkeyvalues TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1ecnamesearchkeyvalues TO csgdeptuser;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1ecnamesearchkeyvalues TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1ecnamesearchkeyvalues TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1ecnamesearchkeyvalues TO sachinahana;


--
-- Name: TABLE k1ecpropertysearchkeyvalues; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1ecpropertysearchkeyvalues TO csgk2user;
GRANT ALL ON TABLE k1data.k1ecpropertysearchkeyvalues TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE k1data.k1ecpropertysearchkeyvalues TO csgadmin;
GRANT ALL ON TABLE k1data.k1ecpropertysearchkeyvalues TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1ecpropertysearchkeyvalues TO csgdeptuser;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE k1data.k1ecpropertysearchkeyvalues TO csgkaverirwx;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE k1data.k1ecpropertysearchkeyvalues TO csgmig;
GRANT ALL ON TABLE k1data.k1ecpropertysearchkeyvalues TO csgreplica;
GRANT SELECT,REFERENCES ON TABLE k1data.k1ecpropertysearchkeyvalues TO csgusermis;
GRANT SELECT,REFERENCES ON TABLE k1data.k1ecpropertysearchkeyvalues TO jslip;
GRANT ALL ON TABLE k1data.k1ecpropertysearchkeyvalues TO malathi_s;
GRANT ALL ON TABLE k1data.k1ecpropertysearchkeyvalues TO raghavendra;
GRANT SELECT,REFERENCES ON TABLE k1data.k1ecpropertysearchkeyvalues TO sshuser;
GRANT ALL ON TABLE k1data.k1ecpropertysearchkeyvalues TO test_user;
GRANT ALL ON TABLE k1data.k1ecpropertysearchkeyvalues TO vijaylakshmi;
GRANT SELECT ON TABLE k1data.k1ecpropertysearchkeyvalues TO ramachandrak;
GRANT SELECT ON TABLE k1data.k1ecpropertysearchkeyvalues TO pavitra;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1ecpropertysearchkeyvalues TO abhijeet;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1ecpropertysearchkeyvalues TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1ecpropertysearchkeyvalues TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1ecpropertysearchkeyvalues TO sachinahana;


--
-- Name: SEQUENCE k1partyinfo_partyid_seq; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE k1data.k1partyinfo_partyid_seq TO csgk2user;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_partyid_seq TO sumit WITH GRANT OPTION;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_partyid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_partyid_seq TO csgdeptuser;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_partyid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_partyid_seq TO csgmig;
GRANT SELECT ON SEQUENCE k1data.k1partyinfo_partyid_seq TO csgusermis;
GRANT SELECT,USAGE ON SEQUENCE k1data.k1partyinfo_partyid_seq TO jslip;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_partyid_seq TO raghavendra;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_partyid_seq TO sshuser;
GRANT SELECT,USAGE ON SEQUENCE k1data.k1partyinfo_partyid_seq TO test_user;
GRANT SELECT,USAGE ON SEQUENCE k1data.k1partyinfo_partyid_seq TO vijaylakshmi;


--
-- Name: TABLE k1partyinfo; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1partyinfo TO csgk2user;
GRANT ALL ON TABLE k1data.k1partyinfo TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE k1data.k1partyinfo TO ramachandrak;
GRANT SELECT ON TABLE k1data.k1partyinfo TO vijaylakshmi;
GRANT SELECT ON TABLE k1data.k1partyinfo TO pavitra;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo TO abhijeet;
GRANT SELECT,REFERENCES ON TABLE k1data.k1partyinfo TO test_user;
GRANT SELECT,REFERENCES ON TABLE k1data.k1partyinfo TO sshuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo TO csgdeptuser;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo TO sachinahana;


--
-- Name: TABLE k1partyinfo_updatetest; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1partyinfo_updatetest TO csgk2user;
GRANT SELECT ON TABLE k1data.k1partyinfo_updatetest TO ramachandrak;
GRANT ALL ON TABLE k1data.k1partyinfo_updatetest TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE k1data.k1partyinfo_updatetest TO pavitra;
GRANT SELECT ON TABLE k1data.k1partyinfo_updatetest TO deptdba;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo_updatetest TO abhijeet;
GRANT SELECT,REFERENCES ON TABLE k1data.k1partyinfo_updatetest TO test_user;
GRANT SELECT,REFERENCES ON TABLE k1data.k1partyinfo_updatetest TO sshuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo_updatetest TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo_updatetest TO csgdeptuser;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo_updatetest TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo_updatetest TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1partyinfo_updatetest TO sachinahana;


--
-- Name: SEQUENCE k1partyinfo_updatetest_surid_seq; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT ON SEQUENCE k1data.k1partyinfo_updatetest_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_updatetest_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE k1data.k1partyinfo_updatetest_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_updatetest_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE k1data.k1partyinfo_updatetest_surid_seq TO csgdeptuser;


--
-- Name: TABLE k1propertymaster; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1propertymaster TO csgk2user;
GRANT ALL ON TABLE k1data.k1propertymaster TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE k1data.k1propertymaster TO csgadmin;
GRANT ALL ON TABLE k1data.k1propertymaster TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1propertymaster TO csgdeptuser;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE k1data.k1propertymaster TO csgkaverirwx;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE k1data.k1propertymaster TO csgmig;
GRANT ALL ON TABLE k1data.k1propertymaster TO csgreplica;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertymaster TO csgusermis;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertymaster TO jslip;
GRANT ALL ON TABLE k1data.k1propertymaster TO malathi_s;
GRANT ALL ON TABLE k1data.k1propertymaster TO raghavendra;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertymaster TO sshuser;
GRANT ALL ON TABLE k1data.k1propertymaster TO test_user;
GRANT ALL ON TABLE k1data.k1propertymaster TO vijaylakshmi;
GRANT SELECT ON TABLE k1data.k1propertymaster TO ramachandrak;
GRANT SELECT ON TABLE k1data.k1propertymaster TO pavitra;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertymaster TO abhijeet;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertymaster TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertymaster TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertymaster TO sachinahana;


--
-- Name: TABLE k1propertynumberdetails; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1propertynumberdetails TO csgk2user;
GRANT ALL ON TABLE k1data.k1propertynumberdetails TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE k1data.k1propertynumberdetails TO csgadmin;
GRANT ALL ON TABLE k1data.k1propertynumberdetails TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1propertynumberdetails TO csgdeptuser;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE k1data.k1propertynumberdetails TO csgkaverirwx;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE k1data.k1propertynumberdetails TO csgmig;
GRANT ALL ON TABLE k1data.k1propertynumberdetails TO csgreplica;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertynumberdetails TO csgusermis;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertynumberdetails TO jslip;
GRANT ALL ON TABLE k1data.k1propertynumberdetails TO malathi_s;
GRANT ALL ON TABLE k1data.k1propertynumberdetails TO raghavendra;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertynumberdetails TO sshuser;
GRANT ALL ON TABLE k1data.k1propertynumberdetails TO test_user;
GRANT ALL ON TABLE k1data.k1propertynumberdetails TO vijaylakshmi;
GRANT SELECT ON TABLE k1data.k1propertynumberdetails TO ramachandrak;
GRANT SELECT ON TABLE k1data.k1propertynumberdetails TO pavitra;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertynumberdetails TO abhijeet;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertynumberdetails TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertynumberdetails TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertynumberdetails TO sachinahana;


--
-- Name: TABLE k1propertynumberdetails_new1; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1propertynumberdetails_new1 TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertynumberdetails_new1 TO sshuser;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertynumberdetails_new1 TO test_user;
GRANT SELECT ON TABLE k1data.k1propertynumberdetails_new1 TO ramachandrak;
GRANT ALL ON TABLE k1data.k1propertynumberdetails_new1 TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE k1data.k1propertynumberdetails_new1 TO pavitra;
GRANT SELECT ON TABLE k1data.k1propertynumberdetails_new1 TO deptdba;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertynumberdetails_new1 TO abhijeet;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertynumberdetails_new1 TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertynumberdetails_new1 TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertynumberdetails_new1 TO sachinahana;


--
-- Name: SEQUENCE k1propertynumberdetails_new1_surid_seq; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT ON SEQUENCE k1data.k1propertynumberdetails_new1_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE k1data.k1propertynumberdetails_new1_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE k1data.k1propertynumberdetails_new1_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE k1data.k1propertynumberdetails_new1_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE k1data.k1propertynumberdetails_new1_surid_seq TO csgdeptuser;


--
-- Name: TABLE k1propertyschedules; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1propertyschedules TO csgk2user;
GRANT ALL ON TABLE k1data.k1propertyschedules TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE k1data.k1propertyschedules TO csgadmin;
GRANT ALL ON TABLE k1data.k1propertyschedules TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.k1propertyschedules TO csgdeptuser;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE k1data.k1propertyschedules TO csgkaverirwx;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE k1data.k1propertyschedules TO csgmig;
GRANT ALL ON TABLE k1data.k1propertyschedules TO csgreplica;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertyschedules TO csgusermis;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertyschedules TO jslip;
GRANT ALL ON TABLE k1data.k1propertyschedules TO malathi_s;
GRANT ALL ON TABLE k1data.k1propertyschedules TO raghavendra;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertyschedules TO sshuser;
GRANT ALL ON TABLE k1data.k1propertyschedules TO test_user;
GRANT ALL ON TABLE k1data.k1propertyschedules TO vijaylakshmi;
GRANT SELECT ON TABLE k1data.k1propertyschedules TO ramachandrak;
GRANT SELECT ON TABLE k1data.k1propertyschedules TO pavitra;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertyschedules TO abhijeet;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertyschedules TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertyschedules TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertyschedules TO sachinahana;


--
-- Name: TABLE k1propertyschedules_new_1; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.k1propertyschedules_new_1 TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertyschedules_new_1 TO sshuser;
GRANT SELECT,REFERENCES ON TABLE k1data.k1propertyschedules_new_1 TO test_user;
GRANT SELECT ON TABLE k1data.k1propertyschedules_new_1 TO ramachandrak;
GRANT ALL ON TABLE k1data.k1propertyschedules_new_1 TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE k1data.k1propertyschedules_new_1 TO pavitra;
GRANT SELECT ON TABLE k1data.k1propertyschedules_new_1 TO deptdba;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertyschedules_new_1 TO abhijeet;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertyschedules_new_1 TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertyschedules_new_1 TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.k1propertyschedules_new_1 TO sachinahana;


--
-- Name: SEQUENCE k1propertyschedules_new_1_surid_seq; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT ON SEQUENCE k1data.k1propertyschedules_new_1_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE k1data.k1propertyschedules_new_1_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE k1data.k1propertyschedules_new_1_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE k1data.k1propertyschedules_new_1_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE k1data.k1propertyschedules_new_1_surid_seq TO csgdeptuser;


--
-- Name: SEQUENCE k1propertyschedules_surid_seq; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT ON SEQUENCE k1data.k1propertyschedules_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE k1data.k1propertyschedules_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE k1data.k1propertyschedules_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE k1data.k1propertyschedules_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE k1data.k1propertyschedules_surid_seq TO csgdeptuser;


--
-- Name: TABLE propertymaster_new2; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.propertymaster_new2 TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE k1data.propertymaster_new2 TO sshuser;
GRANT SELECT,REFERENCES ON TABLE k1data.propertymaster_new2 TO test_user;
GRANT SELECT ON TABLE k1data.propertymaster_new2 TO ramachandrak;
GRANT ALL ON TABLE k1data.propertymaster_new2 TO sumit WITH GRANT OPTION;
GRANT SELECT ON TABLE k1data.propertymaster_new2 TO pavitra;
GRANT SELECT ON TABLE k1data.propertymaster_new2 TO deptdba;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.propertymaster_new2 TO abhijeet;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.propertymaster_new2 TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.propertymaster_new2 TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.propertymaster_new2 TO sachinahana;


--
-- Name: SEQUENCE propertymaster_new2_surid_seq; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT ON SEQUENCE k1data.propertymaster_new2_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE k1data.propertymaster_new2_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE k1data.propertymaster_new2_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE k1data.propertymaster_new2_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE k1data.propertymaster_new2_surid_seq TO csgdeptuser;


--
-- Name: TABLE villagemastervillagesmergingmappping; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT,REFERENCES ON TABLE k1data.villagemastervillagesmergingmappping TO csgk2user;
GRANT ALL ON TABLE k1data.villagemastervillagesmergingmappping TO sumit WITH GRANT OPTION;
GRANT ALL ON TABLE k1data.villagemastervillagesmergingmappping TO csgadmin;
GRANT ALL ON TABLE k1data.villagemastervillagesmergingmappping TO csgcitizenuser;
GRANT SELECT,INSERT,REFERENCES,UPDATE ON TABLE k1data.villagemastervillagesmergingmappping TO csgdeptuser;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE k1data.villagemastervillagesmergingmappping TO csgkaverirwx;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE k1data.villagemastervillagesmergingmappping TO csgmig;
GRANT ALL ON TABLE k1data.villagemastervillagesmergingmappping TO csgreplica;
GRANT SELECT,REFERENCES ON TABLE k1data.villagemastervillagesmergingmappping TO csgusermis;
GRANT SELECT,REFERENCES ON TABLE k1data.villagemastervillagesmergingmappping TO jslip;
GRANT ALL ON TABLE k1data.villagemastervillagesmergingmappping TO malathi_s;
GRANT ALL ON TABLE k1data.villagemastervillagesmergingmappping TO raghavendra;
GRANT SELECT,REFERENCES ON TABLE k1data.villagemastervillagesmergingmappping TO sshuser;
GRANT ALL ON TABLE k1data.villagemastervillagesmergingmappping TO test_user;
GRANT ALL ON TABLE k1data.villagemastervillagesmergingmappping TO vijaylakshmi;
GRANT SELECT ON TABLE k1data.villagemastervillagesmergingmappping TO ramachandrak;
GRANT SELECT ON TABLE k1data.villagemastervillagesmergingmappping TO pavitra;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.villagemastervillagesmergingmappping TO abhijeet;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.villagemastervillagesmergingmappping TO venkat;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.villagemastervillagesmergingmappping TO chethanahana;
GRANT SELECT,REFERENCES,UPDATE ON TABLE k1data.villagemastervillagesmergingmappping TO sachinahana;


--
-- Name: SEQUENCE villagemastervillagesmergingmappping_surid_seq; Type: ACL; Schema: k1data; Owner: postgres
--

GRANT SELECT ON SEQUENCE k1data.villagemastervillagesmergingmappping_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE k1data.villagemastervillagesmergingmappping_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE k1data.villagemastervillagesmergingmappping_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE k1data.villagemastervillagesmergingmappping_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE k1data.villagemastervillagesmergingmappping_surid_seq TO csgdeptuser;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: k1data; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA k1data GRANT SELECT,REFERENCES ON TABLES  TO csgk2user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA k1data GRANT SELECT,REFERENCES ON TABLES  TO sshuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA k1data GRANT SELECT,REFERENCES ON TABLES  TO test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA k1data GRANT SELECT ON TABLES  TO ramachandrak;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA k1data GRANT SELECT ON TABLES  TO pavitra;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA k1data GRANT SELECT,REFERENCES,UPDATE ON TABLES  TO abhijeet;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA k1data GRANT SELECT,REFERENCES,UPDATE ON TABLES  TO venkat;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA k1data GRANT SELECT,REFERENCES,UPDATE ON TABLES  TO sachinahana;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA k1data GRANT SELECT,REFERENCES,UPDATE ON TABLES  TO chethanahana;


--
-- PostgreSQL database dump complete
--

