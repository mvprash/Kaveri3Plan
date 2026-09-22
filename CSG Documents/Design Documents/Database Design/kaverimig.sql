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
-- Name: kaverimig; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA kaverimig;


ALTER SCHEMA kaverimig OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ams_bankinstrumentnumberdetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.ams_bankinstrumentnumberdetails_reject (
    row_id integer NOT NULL,
    instrumentnumber character varying(100),
    instrumentdate date,
    stamptypeid integer,
    receiptpaymentmode bigint,
    receiptid bigint,
    stampdetailsid bigint,
    receiptnumber integer,
    receipt_stampdate timestamp without time zone,
    srocode integer,
    drocode integer,
    isdro integer,
    uniquereqid numeric,
    inserteddatetime timestamp without time zone,
    sourceofreceipt character varying(100),
    isthroughsyncoperation integer,
    amount numeric,
    serviceid integer,
    documentid bigint,
    documentpendingnumber character varying(100),
    partyname character varying(1000),
    jobid bigint
);


ALTER TABLE kaverimig.ams_bankinstrumentnumberdetails_reject OWNER TO csgadmin;

--
-- Name: app; Type: TABLE; Schema: kaverimig; Owner: postgres
--

CREATE TABLE kaverimig.app (
    id bigint,
    service_id bigint,
    queue_id bigint,
    applicationnumber character varying(50),
    status smallint,
    queue_data text,
    inserted_date timestamp without time zone,
    srocode integer,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.app OWNER TO postgres;

--
-- Name: app_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: postgres
--

CREATE SEQUENCE kaverimig.app_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.app_surid_seq OWNER TO postgres;

--
-- Name: app_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: postgres
--

ALTER SEQUENCE kaverimig.app_surid_seq OWNED BY kaverimig.app.surid;


--
-- Name: bannedproperties_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.bannedproperties_reject (
    propertyid bigint,
    srocode integer,
    orderid bigint,
    jurisdictionsrcode integer,
    villagecode bigint,
    propertydescription character varying(1000),
    isagriculturalproperty boolean,
    northboundary character varying(500),
    southboundary character varying(500),
    eastboundary character varying(500),
    westboundary character varying(500),
    extentinformation character varying(500),
    area numeric(18,4),
    measurementunit integer,
    courtpropertyid bigint,
    orderid_old bigint,
    isdelete boolean,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.bannedproperties_reject OWNER TO csgadmin;

--
-- Name: bannedproperties_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.bannedproperties_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.bannedproperties_reject_surid_seq OWNER TO csgadmin;

--
-- Name: bannedproperties_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.bannedproperties_reject_surid_seq OWNED BY kaverimig.bannedproperties_reject.surid;


--
-- Name: bannedpropertynumbers_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.bannedpropertynumbers_reject (
    id bigint,
    srocode integer NOT NULL,
    propertyid bigint,
    orderid bigint,
    currentpropertytypeid integer,
    currentnumber character varying(300),
    oldpropertytypeid integer,
    oldnumber character varying(300),
    description character varying(1000),
    survey_no integer,
    surnoc character varying(20),
    hissa_no character varying(30),
    injuction_or_stay_flag character varying,
    courtpropertynumberid bigint NOT NULL,
    orderid_old bigint,
    propertyid_old bigint,
    isdelete boolean DEFAULT false,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.bannedpropertynumbers_reject OWNER TO csgadmin;

--
-- Name: bannedpropertynumbers_reject_courtpropertynumberid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.bannedpropertynumbers_reject_courtpropertynumberid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.bannedpropertynumbers_reject_courtpropertynumberid_seq OWNER TO csgadmin;

--
-- Name: bannedpropertynumbers_reject_courtpropertynumberid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.bannedpropertynumbers_reject_courtpropertynumberid_seq OWNED BY kaverimig.bannedpropertynumbers_reject.courtpropertynumberid;


--
-- Name: bannedpropertynumbers_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.bannedpropertynumbers_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.bannedpropertynumbers_reject_surid_seq OWNER TO csgadmin;

--
-- Name: bannedpropertynumbers_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.bannedpropertynumbers_reject_surid_seq OWNED BY kaverimig.bannedpropertynumbers_reject.surid;


--
-- Name: cc_applicationdetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.cc_applicationdetails_reject (
    ccid bigint,
    ccnumber character varying(50),
    ccdate timestamp without time zone,
    userid bigint,
    documenttype smallint,
    kaveridrocode integer,
    kaverisrocode integer,
    documentnumber character varying(50),
    booktype smallint,
    yearofregistration character varying(50),
    pagecount integer,
    totalamount numeric(18,0),
    isappliedforsignedcopy boolean,
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
    k1k2_flag smallint,
    inserteddatetime timestamp without time zone,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.cc_applicationdetails_reject OWNER TO csgadmin;

--
-- Name: cc_applicationdetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.cc_applicationdetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.cc_applicationdetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: cc_applicationdetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.cc_applicationdetails_reject_surid_seq OWNED BY kaverimig.cc_applicationdetails_reject.surid;


--
-- Name: cc_esignfilepath_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.cc_esignfilepath_reject (
    fileid bigint,
    ccid bigint,
    pserverpath character varying(200),
    vserverpath character varying(200),
    esigndatetime timestamp without time zone,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.cc_esignfilepath_reject OWNER TO csgadmin;

--
-- Name: cc_esignfilepath_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.cc_esignfilepath_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.cc_esignfilepath_reject_surid_seq OWNER TO csgadmin;

--
-- Name: cc_esignfilepath_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.cc_esignfilepath_reject_surid_seq OWNED BY kaverimig.cc_esignfilepath_reject.surid;


--
-- Name: cc_qrcodedetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.cc_qrcodedetails_reject (
    qrcodeid bigint,
    ccdocumentid bigint,
    qrencryptkey character varying(200),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.cc_qrcodedetails_reject OWNER TO csgadmin;

--
-- Name: cc_qrcodedetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.cc_qrcodedetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.cc_qrcodedetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: cc_qrcodedetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.cc_qrcodedetails_reject_surid_seq OWNED BY kaverimig.cc_qrcodedetails_reject.surid;


--
-- Name: cc_signedfilepaths_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.cc_signedfilepaths_reject (
    fileid bigint,
    ccid bigint,
    preparedfserverpath character varying(200),
    preparedvserverpath character varying(200),
    prepareddatetime timestamp without time zone,
    comparedfserverpath character varying(200),
    comparedvserverpath character varying(200),
    compareddatetime timestamp without time zone,
    signedfserverpath character varying(200),
    signedvserverpath character varying(200),
    signeddatetime timestamp without time zone,
    preparedreferencenumber character varying(200),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.cc_signedfilepaths_reject OWNER TO csgadmin;

--
-- Name: cc_signedfilepaths_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.cc_signedfilepaths_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.cc_signedfilepaths_reject_surid_seq OWNER TO csgadmin;

--
-- Name: cc_signedfilepaths_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.cc_signedfilepaths_reject_surid_seq OWNED BY kaverimig.cc_signedfilepaths_reject.surid;


--
-- Name: courtorders_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.courtorders_reject (
    orderid bigint,
    srocode integer,
    ordernumber character varying(1000),
    issuingauthority character varying(1000),
    issueddate timestamp without time zone,
    description character varying(5000),
    regactarticle integer,
    dateofcancellation timestamp without time zone,
    reasonofcancellation character varying(1000),
    iscancelled boolean,
    isinforce boolean,
    orderentrydatetime timestamp without time zone,
    cancellationorderno character varying(200),
    cancellationdate timestamp without time zone,
    cancelledby integer,
    cancellationremarks character varying(2000),
    username character varying(50),
    courtorderid bigint,
    casetype character varying(200),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.courtorders_reject OWNER TO csgadmin;

--
-- Name: courtorders_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.courtorders_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.courtorders_reject_surid_seq OWNER TO csgadmin;

--
-- Name: courtorders_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.courtorders_reject_surid_seq OWNED BY kaverimig.courtorders_reject.surid;


--
-- Name: districtmaster_new_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.districtmaster_new_reject (
    talukcode integer,
    districtcode integer,
    taluknamek character varying(150),
    taluknamee character varying(150),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.districtmaster_new_reject OWNER TO csgadmin;

--
-- Name: districtmaster_new_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.districtmaster_new_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.districtmaster_new_reject_surid_seq OWNER TO csgadmin;

--
-- Name: districtmaster_new_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.districtmaster_new_reject_surid_seq OWNED BY kaverimig.districtmaster_new_reject.surid;


--
-- Name: ec_applicationdetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.ec_applicationdetails_reject (
    ecid bigint,
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
    eastboundary character varying(100),
    westboundary character varying(100),
    northboundary character varying(100),
    southboundary character varying(100),
    easttowest character varying(100),
    northtosouth character varying(100),
    remarktoreprepareec character varying(200),
    area numeric(18,0),
    propertydescription character varying(200),
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
    k1k2_flag smallint,
    inserteddatetime timestamp without time zone,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.ec_applicationdetails_reject OWNER TO csgadmin;

--
-- Name: ec_applicationdetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.ec_applicationdetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.ec_applicationdetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: ec_applicationdetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.ec_applicationdetails_reject_surid_seq OWNED BY kaverimig.ec_applicationdetails_reject.surid;


--
-- Name: ec_esignfilepath_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.ec_esignfilepath_reject (
    fileid bigint,
    ecid bigint,
    pserverpath character varying(200),
    vserverpath character varying(200),
    esigndatetime timestamp without time zone,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.ec_esignfilepath_reject OWNER TO csgadmin;

--
-- Name: ec_esignfilepath_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.ec_esignfilepath_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.ec_esignfilepath_reject_surid_seq OWNER TO csgadmin;

--
-- Name: ec_esignfilepath_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.ec_esignfilepath_reject_surid_seq OWNED BY kaverimig.ec_esignfilepath_reject.surid;


--
-- Name: ec_qrcodedetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.ec_qrcodedetails_reject (
    qrcodeid bigint,
    ecid bigint,
    qrencryptkey character varying(200),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.ec_qrcodedetails_reject OWNER TO csgadmin;

--
-- Name: ec_qrcodedetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.ec_qrcodedetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.ec_qrcodedetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: ec_qrcodedetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.ec_qrcodedetails_reject_surid_seq OWNED BY kaverimig.ec_qrcodedetails_reject.surid;


--
-- Name: ec_signedfilepaths_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.ec_signedfilepaths_reject (
    fileid bigint,
    ecid bigint,
    preparedfserverpath character varying(200),
    preparedvserverpath character varying(200),
    prepareddatetime timestamp without time zone,
    comparedfserverpath character varying(200),
    comparedvserverpath character varying(200),
    compareddatetime timestamp without time zone,
    signedfserverpath character varying(200),
    signedvserverpath character varying(200),
    signeddatetime timestamp without time zone,
    preparedreferencenumber character varying(200),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.ec_signedfilepaths_reject OWNER TO csgadmin;

--
-- Name: ec_signedfilepaths_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.ec_signedfilepaths_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.ec_signedfilepaths_reject_surid_seq OWNER TO csgadmin;

--
-- Name: ec_signedfilepaths_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.ec_signedfilepaths_reject_surid_seq OWNED BY kaverimig.ec_signedfilepaths_reject.surid;


--
-- Name: ecsearchdocumentnodetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.ecsearchdocumentnodetails_reject (
    ecsearchdocumentid bigint,
    applicationid bigint,
    srocode integer,
    bookid integer,
    documentnumber integer,
    registrationyear character varying(7),
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.ecsearchdocumentnodetails_reject OWNER TO csgadmin;

--
-- Name: ecsearchdocumentnodetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.ecsearchdocumentnodetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.ecsearchdocumentnodetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: ecsearchdocumentnodetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.ecsearchdocumentnodetails_reject_surid_seq OWNED BY kaverimig.ecsearchdocumentnodetails_reject.surid;


--
-- Name: ecsearchpartydetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.ecsearchpartydetails_reject (
    ecsearchpartyid bigint,
    applicationid bigint,
    srocode integer,
    partytypeid integer,
    partyname character varying(100),
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.ecsearchpartydetails_reject OWNER TO csgadmin;

--
-- Name: ecsearchpartydetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.ecsearchpartydetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.ecsearchpartydetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: ecsearchpartydetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.ecsearchpartydetails_reject_surid_seq OWNED BY kaverimig.ecsearchpartydetails_reject.surid;


--
-- Name: ecsearchpropertynodetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.ecsearchpropertynodetails_reject (
    ecsearchproperty bigint,
    applicationid bigint,
    srocode integer,
    propertynotypeid integer,
    currentpropertynumber character varying(75),
    oldpropertynumber character varying(75),
    surveynumber character varying(10),
    surveychar character varying(20),
    surveyhissa character varying(30),
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.ecsearchpropertynodetails_reject OWNER TO csgadmin;

--
-- Name: ecsearchpropertynodetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.ecsearchpropertynodetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.ecsearchpropertynodetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: ecsearchpropertynodetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.ecsearchpropertynodetails_reject_surid_seq OWNED BY kaverimig.ecsearchpropertynodetails_reject.surid;


--
-- Name: hoblimaster_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.hoblimaster_reject (
    hoblicode integer,
    talukcode integer,
    hoblinamek character varying(500),
    hoblinamee character varying(500),
    shortnamek character varying(5),
    shortnamee character varying(5),
    bhoomihoblicode integer,
    bhoomihobliname character varying(100),
    bhoomitalukcode integer,
    bhoomitalukname character varying(100),
    bhoomidistrictcode integer,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.hoblimaster_reject OWNER TO csgadmin;

--
-- Name: hoblimaster_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.hoblimaster_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.hoblimaster_reject_surid_seq OWNER TO csgadmin;

--
-- Name: hoblimaster_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.hoblimaster_reject_surid_seq OWNED BY kaverimig.hoblimaster_reject.surid;


--
-- Name: jobstatus; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.jobstatus (
    jobid bigint NOT NULL,
    batchsize bigint,
    sourcetablename character varying(100) NOT NULL,
    sourcecount_total integer,
    sourcecount_current_batch integer,
    targettablename character varying(100) NOT NULL,
    targetcount_migrated integer,
    targetcount_current_batch integer,
    rejectedcount integer,
    jobstartdate timestamp without time zone,
    jobenddate timestamp without time zone,
    duration bigint,
    status character varying(10),
    minvalue bigint,
    maxvalue bigint,
    targetcount_updated integer,
    stg_countinserted integer,
    stg_countupdated integer,
    stg_countrejected integer,
    stg_count_current_batch integer
);


ALTER TABLE kaverimig.jobstatus OWNER TO csgadmin;

--
-- Name: jobstatus_jobid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE kaverimig.jobstatus ALTER COLUMN jobid ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME kaverimig.jobstatus_jobid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1
);


--
-- Name: liabilitydetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.liabilitydetails_reject (
    liabilityfromdate timestamp without time zone,
    liabilityadditionalnote character varying(500),
    liabilityid bigint NOT NULL,
    entrydate timestamp without time zone NOT NULL,
    issuedate timestamp without time zone NOT NULL,
    issuedby character varying(50) NOT NULL,
    amount numeric NOT NULL,
    ordernumber character varying(50) NOT NULL,
    liabilitynote character varying NOT NULL,
    srocode integer NOT NULL,
    userid integer NOT NULL,
    drocode integer,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    isdeleted boolean DEFAULT false,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.liabilitydetails_reject OWNER TO csgadmin;

--
-- Name: liabilitydetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.liabilitydetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.liabilitydetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: liabilitydetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.liabilitydetails_reject_surid_seq OWNED BY kaverimig.liabilitydetails_reject.surid;


--
-- Name: liabilityonpropertydetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.liabilityonpropertydetails_reject (
    mappingid bigint,
    srocode1 integer,
    liabilityid bigint,
    documentid bigint,
    propertyid bigint,
    srocode integer,
    ordernumber character varying(50),
    orderissuedate timestamp without time zone,
    note character varying(1000),
    amount numeric(23,4),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.liabilityonpropertydetails_reject OWNER TO csgadmin;

--
-- Name: liabilityonpropertydetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.liabilityonpropertydetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.liabilityonpropertydetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: liabilityonpropertydetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.liabilityonpropertydetails_reject_surid_seq OWNED BY kaverimig.liabilityonpropertydetails_reject.surid;


--
-- Name: liabilitypropertymapped_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.liabilitypropertymapped_reject (
    mappedid bigint,
    liabilityid bigint,
    documentid bigint,
    propertyid bigint,
    ispropertysearched boolean,
    srocode integer,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.liabilitypropertymapped_reject OWNER TO csgadmin;

--
-- Name: liabilitypropertymapped_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.liabilitypropertymapped_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.liabilitypropertymapped_reject_surid_seq OWNER TO csgadmin;

--
-- Name: liabilitypropertymapped_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.liabilitypropertymapped_reject_surid_seq OWNED BY kaverimig.liabilitypropertymapped_reject.surid;


--
-- Name: logdetails; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.logdetails (
    moment timestamp without time zone NOT NULL,
    jobid integer,
    pid character varying(20),
    root_pid character varying(20),
    father_pid character varying(20),
    project character varying(50),
    job character varying(255),
    context character varying(50),
    priority integer,
    type character varying(255),
    origin character varying(255),
    message character varying(255),
    code integer
);


ALTER TABLE kaverimig.logdetails OWNER TO csgadmin;

--
-- Name: openbuiltratedetail_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.openbuiltratedetail_reject (
    villagecode bigint,
    roadcode bigint,
    propertytypeid integer,
    rate numeric(18,5),
    measurementcode integer,
    effectivedate timestamp without time zone,
    openbuildratecode bigint,
    k1k2_flag smallint,
    inserteddatetime timestamp without time zone,
    prevrate numeric(18,5),
    prevrate2 numeric(18,5),
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.openbuiltratedetail_reject OWNER TO csgadmin;

--
-- Name: openbuiltratedetail_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.openbuiltratedetail_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.openbuiltratedetail_reject_surid_seq OWNER TO csgadmin;

--
-- Name: openbuiltratedetail_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.openbuiltratedetail_reject_surid_seq OWNED BY kaverimig.openbuiltratedetail_reject.surid;


--
-- Name: partyinfo_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.partyinfo_reject (
    partyid bigint NOT NULL,
    srocode integer NOT NULL,
    documentid bigint NOT NULL,
    partytypeid integer NOT NULL,
    firstname character varying(300),
    middlename character varying(100),
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
    availableextfgunta integer,
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
    totalextfgunta integer,
    transactextacre integer,
    transactextgunta integer,
    transactextfgunta integer,
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
    isprivateattendance boolean,
    coveringletterno character(100),
    section88file character(500),
    isendorseprinted boolean DEFAULT false,
    thumbremarks character varying(200),
    partyidreference bigint,
    inserteddatetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    k1k2_flag smallint DEFAULT 2,
    ispartyrefused boolean DEFAULT false,
    age_k1 character varying(50),
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.partyinfo_reject OWNER TO csgadmin;

--
-- Name: partyinfo_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.partyinfo_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.partyinfo_reject_surid_seq OWNER TO csgadmin;

--
-- Name: partyinfo_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.partyinfo_reject_surid_seq OWNED BY kaverimig.partyinfo_reject.surid;


--
-- Name: propertymaster_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.propertymaster_reject (
    propertyid bigint,
    documentid bigint,
    villagecode bigint,
    regsrocode integer,
    srocode integer,
    totalarea numeric(18,4),
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
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.propertymaster_reject OWNER TO csgadmin;

--
-- Name: propertymaster_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.propertymaster_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.propertymaster_reject_surid_seq OWNER TO csgadmin;

--
-- Name: propertymaster_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.propertymaster_reject_surid_seq OWNED BY kaverimig.propertymaster_reject.surid;


--
-- Name: propertyschedules_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.propertyschedules_reject (
    scheduleid bigint,
    propertyid bigint,
    srocode integer,
    partyid bigint,
    scheduletype character varying(3),
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
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.propertyschedules_reject OWNER TO csgadmin;

--
-- Name: propertyschedules_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.propertyschedules_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.propertyschedules_reject_surid_seq OWNER TO csgadmin;

--
-- Name: propertyschedules_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.propertyschedules_reject_surid_seq OWNED BY kaverimig.propertyschedules_reject.surid;


--
-- Name: rateagriculturaldetail_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.rateagriculturaldetail_reject (
    roadcode bigint,
    agrilandtypeid integer,
    villagecode bigint,
    measurementcode integer,
    rate numeric(18,5),
    effectivedate timestamp without time zone,
    rateagricode bigint,
    k1k2_flag smallint,
    inserteddatetime timestamp without time zone,
    prevrate numeric(18,5),
    prevrate2 numeric(18,5),
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.rateagriculturaldetail_reject OWNER TO csgadmin;

--
-- Name: rateagriculturaldetail_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.rateagriculturaldetail_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.rateagriculturaldetail_reject_surid_seq OWNER TO csgadmin;

--
-- Name: rateagriculturaldetail_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.rateagriculturaldetail_reject_surid_seq OWNED BY kaverimig.rateagriculturaldetail_reject.surid;


--
-- Name: roadmaster_new_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.roadmaster_new_reject (
    roadcode bigint,
    roadnamee character varying(2000),
    roadnamek character varying(2000),
    villagecode bigint,
    roadref bigint,
    isactive boolean,
    regionid integer,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.roadmaster_new_reject OWNER TO csgadmin;

--
-- Name: roadmaster_new_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.roadmaster_new_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.roadmaster_new_reject_surid_seq OWNER TO csgadmin;

--
-- Name: roadmaster_new_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.roadmaster_new_reject_surid_seq OWNED BY kaverimig.roadmaster_new_reject.surid;


--
-- Name: sromaster_new_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.sromaster_new_reject (
    srocode integer,
    districtcode integer,
    sronamek character varying(100),
    sronamee character varying(150),
    shortnamek character varying(50),
    shortnamee character varying(15),
    enableanywherereg boolean,
    getbhoomidata boolean,
    registrationdocserial bigint,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.sromaster_new_reject OWNER TO csgadmin;

--
-- Name: sromaster_new_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.sromaster_new_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.sromaster_new_reject_surid_seq OWNER TO csgadmin;

--
-- Name: sromaster_new_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.sromaster_new_reject_surid_seq OWNED BY kaverimig.sromaster_new_reject.surid;


--
-- Name: surveynodetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.surveynodetails_reject (
    surevynocode numeric(10,0),
    categorycode integer,
    surevynumber character varying(1500),
    villagecode numeric(10,0),
    roadcode numeric(10,0),
    surnumber integer,
    surnoc character varying(200),
    hissano character varying(200),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.surveynodetails_reject OWNER TO csgadmin;

--
-- Name: surveynodetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.surveynodetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.surveynodetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: surveynodetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.surveynodetails_reject_surid_seq OWNED BY kaverimig.surveynodetails_reject.surid;


--
-- Name: talukmaster_new_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.talukmaster_new_reject (
    talukcode integer,
    districtcode integer,
    taluknamek character varying(150),
    taluknamee character varying(150),
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.talukmaster_new_reject OWNER TO csgadmin;

--
-- Name: talukmaster_new_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.talukmaster_new_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.talukmaster_new_reject_surid_seq OWNER TO csgadmin;

--
-- Name: talukmaster_new_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.talukmaster_new_reject_surid_seq OWNED BY kaverimig.talukmaster_new_reject.surid;


--
-- Name: val_agriculturedetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.val_agriculturedetails_reject (
    agriculturedetailsid bigint,
    agrilandtypeid smallint,
    unitid integer,
    valuationid bigint,
    verified boolean,
    agrirateid bigint,
    rate numeric(18,2),
    srocode integer,
    regsrocode integer,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.val_agriculturedetails_reject OWNER TO csgadmin;

--
-- Name: val_agriculturedetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.val_agriculturedetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.val_agriculturedetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: val_agriculturedetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.val_agriculturedetails_reject_surid_seq OWNED BY kaverimig.val_agriculturedetails_reject.surid;


--
-- Name: val_annexuredetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.val_annexuredetails_reject (
    annexuredetailsid bigint,
    annexureid smallint,
    area integer,
    rate numeric(15,2),
    valuationid bigint,
    verified boolean,
    srocode integer,
    regsrocode integer,
    isselected boolean,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.val_annexuredetails_reject OWNER TO csgadmin;

--
-- Name: val_annexuredetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.val_annexuredetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.val_annexuredetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: val_annexuredetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.val_annexuredetails_reject_surid_seq OWNED BY kaverimig.val_annexuredetails_reject.surid;


--
-- Name: val_apartmentamenitydetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.val_apartmentamenitydetails_reject (
    amenetiesdetailsid bigint,
    apartmentamenetyruleid smallint,
    rate numeric(18,2),
    valuationid bigint,
    verified boolean,
    srocode integer,
    regsrocode integer,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.val_apartmentamenitydetails_reject OWNER TO csgadmin;

--
-- Name: val_apartmentamenitydetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.val_apartmentamenitydetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.val_apartmentamenitydetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: val_apartmentamenitydetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.val_apartmentamenitydetails_reject_surid_seq OWNED BY kaverimig.val_apartmentamenitydetails_reject.surid;


--
-- Name: val_constructionratedetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.val_constructionratedetails_reject (
    constructiondetailsid bigint,
    constructiontypeid smallint,
    gfarea integer,
    agfarea integer,
    rate numeric(15,2),
    verified boolean,
    valuationid bigint,
    srocode integer,
    regsrocode integer,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.val_constructionratedetails_reject OWNER TO csgadmin;

--
-- Name: val_constructionratedetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.val_constructionratedetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.val_constructionratedetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: val_constructionratedetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.val_constructionratedetails_reject_surid_seq OWNED BY kaverimig.val_constructionratedetails_reject.surid;


--
-- Name: val_flatfloordetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.val_flatfloordetails_reject (
    flatfloordetailsid bigint,
    apartmentfloorrateid smallint,
    rate numeric(18,0),
    verified boolean,
    valuationid bigint,
    srocode integer,
    regsrocode integer,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.val_flatfloordetails_reject OWNER TO csgadmin;

--
-- Name: val_flatfloordetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.val_flatfloordetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.val_flatfloordetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: val_flatfloordetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.val_flatfloordetails_reject_surid_seq OWNED BY kaverimig.val_flatfloordetails_reject.surid;


--
-- Name: val_flatratedetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.val_flatratedetails_reject (
    flatratedetailsid bigint,
    propertytypeid integer,
    amenitiesid integer,
    unitid integer,
    rate numeric(15,2),
    flatrateid integer,
    verified boolean,
    floorid smallint,
    valuationid bigint,
    srocode integer,
    regsrocode integer,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.val_flatratedetails_reject OWNER TO csgadmin;

--
-- Name: val_flatratedetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.val_flatratedetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.val_flatratedetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: val_flatratedetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.val_flatratedetails_reject_surid_seq OWNED BY kaverimig.val_flatratedetails_reject.surid;


--
-- Name: val_openbuiltvaluationdetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.val_openbuiltvaluationdetails_reject (
    openbuiltvalid bigint,
    propertytypeid integer,
    roadid bigint,
    unitid integer,
    rate numeric(15,2),
    valuationid bigint,
    verified boolean,
    openbuiltrateid bigint,
    srocode integer,
    regsrocode integer,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.val_openbuiltvaluationdetails_reject OWNER TO csgadmin;

--
-- Name: val_openbuiltvaluationdetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.val_openbuiltvaluationdetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.val_openbuiltvaluationdetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: val_openbuiltvaluationdetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.val_openbuiltvaluationdetails_reject_surid_seq OWNED BY kaverimig.val_openbuiltvaluationdetails_reject.surid;


--
-- Name: val_parkingratedetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.val_parkingratedetails_reject (
    parkingdetailsid bigint,
    parkingtypeid smallint,
    totalparkings integer,
    rate numeric(15,2),
    verified boolean,
    valuationid bigint,
    srocode integer,
    regsrocode integer,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.val_parkingratedetails_reject OWNER TO csgadmin;

--
-- Name: val_parkingratedetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.val_parkingratedetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.val_parkingratedetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: val_parkingratedetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.val_parkingratedetails_reject_surid_seq OWNED BY kaverimig.val_parkingratedetails_reject.surid;


--
-- Name: valuationdetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.valuationdetails_reject (
    valid bigint,
    srocode integer,
    regsrocode integer,
    villagecode bigint,
    roadcode integer,
    valuationdate timestamp without time zone,
    propertytypeid integer,
    totalarea bigint,
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
    verified boolean,
    issroapproved character varying(1),
    propertyid bigint,
    reportdetails character varying,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.valuationdetails_reject OWNER TO csgadmin;

--
-- Name: valuationdetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.valuationdetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.valuationdetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: valuationdetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.valuationdetails_reject_surid_seq OWNED BY kaverimig.valuationdetails_reject.surid;


--
-- Name: villagemaster_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.villagemaster_reject (
    villagecode bigint,
    srocode integer,
    hoblicode integer,
    censuscode character varying(50),
    talukcode integer,
    villagenamek character varying(500),
    villagenamee character varying(500),
    isurban boolean,
    bhoomitalukcode integer,
    bhoomivillagecode integer,
    bhoomivillagename character varying(100),
    bhoomidistrictcode integer,
    uportownid integer,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    jobid bigint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.villagemaster_reject OWNER TO csgadmin;

--
-- Name: villagemaster_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.villagemaster_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.villagemaster_reject_surid_seq OWNER TO csgadmin;

--
-- Name: villagemaster_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.villagemaster_reject_surid_seq OWNED BY kaverimig.villagemaster_reject.surid;


--
-- Name: warddetails_reject; Type: TABLE; Schema: kaverimig; Owner: csgadmin
--

CREATE TABLE kaverimig.warddetails_reject (
    wardid integer,
    wardnumber character varying(50),
    integrationenabled boolean,
    inserteddatetime timestamp without time zone,
    k1k2_flag smallint,
    surid bigint NOT NULL
);


ALTER TABLE kaverimig.warddetails_reject OWNER TO csgadmin;

--
-- Name: warddetails_reject_surid_seq; Type: SEQUENCE; Schema: kaverimig; Owner: csgadmin
--

CREATE SEQUENCE kaverimig.warddetails_reject_surid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE kaverimig.warddetails_reject_surid_seq OWNER TO csgadmin;

--
-- Name: warddetails_reject_surid_seq; Type: SEQUENCE OWNED BY; Schema: kaverimig; Owner: csgadmin
--

ALTER SEQUENCE kaverimig.warddetails_reject_surid_seq OWNED BY kaverimig.warddetails_reject.surid;


--
-- Name: app surid; Type: DEFAULT; Schema: kaverimig; Owner: postgres
--

ALTER TABLE ONLY kaverimig.app ALTER COLUMN surid SET DEFAULT nextval('kaverimig.app_surid_seq'::regclass);


--
-- Name: bannedproperties_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.bannedproperties_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.bannedproperties_reject_surid_seq'::regclass);


--
-- Name: bannedpropertynumbers_reject courtpropertynumberid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.bannedpropertynumbers_reject ALTER COLUMN courtpropertynumberid SET DEFAULT nextval('kaverimig.bannedpropertynumbers_reject_courtpropertynumberid_seq'::regclass);


--
-- Name: bannedpropertynumbers_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.bannedpropertynumbers_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.bannedpropertynumbers_reject_surid_seq'::regclass);


--
-- Name: cc_applicationdetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.cc_applicationdetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.cc_applicationdetails_reject_surid_seq'::regclass);


--
-- Name: cc_esignfilepath_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.cc_esignfilepath_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.cc_esignfilepath_reject_surid_seq'::regclass);


--
-- Name: cc_qrcodedetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.cc_qrcodedetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.cc_qrcodedetails_reject_surid_seq'::regclass);


--
-- Name: cc_signedfilepaths_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.cc_signedfilepaths_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.cc_signedfilepaths_reject_surid_seq'::regclass);


--
-- Name: courtorders_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.courtorders_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.courtorders_reject_surid_seq'::regclass);


--
-- Name: districtmaster_new_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.districtmaster_new_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.districtmaster_new_reject_surid_seq'::regclass);


--
-- Name: ec_applicationdetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ec_applicationdetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.ec_applicationdetails_reject_surid_seq'::regclass);


--
-- Name: ec_esignfilepath_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ec_esignfilepath_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.ec_esignfilepath_reject_surid_seq'::regclass);


--
-- Name: ec_qrcodedetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ec_qrcodedetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.ec_qrcodedetails_reject_surid_seq'::regclass);


--
-- Name: ec_signedfilepaths_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ec_signedfilepaths_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.ec_signedfilepaths_reject_surid_seq'::regclass);


--
-- Name: ecsearchdocumentnodetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ecsearchdocumentnodetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.ecsearchdocumentnodetails_reject_surid_seq'::regclass);


--
-- Name: ecsearchpartydetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ecsearchpartydetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.ecsearchpartydetails_reject_surid_seq'::regclass);


--
-- Name: ecsearchpropertynodetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ecsearchpropertynodetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.ecsearchpropertynodetails_reject_surid_seq'::regclass);


--
-- Name: hoblimaster_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.hoblimaster_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.hoblimaster_reject_surid_seq'::regclass);


--
-- Name: liabilitydetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.liabilitydetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.liabilitydetails_reject_surid_seq'::regclass);


--
-- Name: liabilityonpropertydetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.liabilityonpropertydetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.liabilityonpropertydetails_reject_surid_seq'::regclass);


--
-- Name: liabilitypropertymapped_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.liabilitypropertymapped_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.liabilitypropertymapped_reject_surid_seq'::regclass);


--
-- Name: openbuiltratedetail_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.openbuiltratedetail_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.openbuiltratedetail_reject_surid_seq'::regclass);


--
-- Name: partyinfo_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.partyinfo_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.partyinfo_reject_surid_seq'::regclass);


--
-- Name: propertymaster_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.propertymaster_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.propertymaster_reject_surid_seq'::regclass);


--
-- Name: propertyschedules_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.propertyschedules_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.propertyschedules_reject_surid_seq'::regclass);


--
-- Name: rateagriculturaldetail_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.rateagriculturaldetail_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.rateagriculturaldetail_reject_surid_seq'::regclass);


--
-- Name: roadmaster_new_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.roadmaster_new_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.roadmaster_new_reject_surid_seq'::regclass);


--
-- Name: sromaster_new_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.sromaster_new_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.sromaster_new_reject_surid_seq'::regclass);


--
-- Name: surveynodetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.surveynodetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.surveynodetails_reject_surid_seq'::regclass);


--
-- Name: talukmaster_new_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.talukmaster_new_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.talukmaster_new_reject_surid_seq'::regclass);


--
-- Name: val_agriculturedetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_agriculturedetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.val_agriculturedetails_reject_surid_seq'::regclass);


--
-- Name: val_annexuredetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_annexuredetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.val_annexuredetails_reject_surid_seq'::regclass);


--
-- Name: val_apartmentamenitydetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_apartmentamenitydetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.val_apartmentamenitydetails_reject_surid_seq'::regclass);


--
-- Name: val_constructionratedetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_constructionratedetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.val_constructionratedetails_reject_surid_seq'::regclass);


--
-- Name: val_flatfloordetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_flatfloordetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.val_flatfloordetails_reject_surid_seq'::regclass);


--
-- Name: val_flatratedetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_flatratedetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.val_flatratedetails_reject_surid_seq'::regclass);


--
-- Name: val_openbuiltvaluationdetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_openbuiltvaluationdetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.val_openbuiltvaluationdetails_reject_surid_seq'::regclass);


--
-- Name: val_parkingratedetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_parkingratedetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.val_parkingratedetails_reject_surid_seq'::regclass);


--
-- Name: valuationdetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.valuationdetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.valuationdetails_reject_surid_seq'::regclass);


--
-- Name: villagemaster_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.villagemaster_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.villagemaster_reject_surid_seq'::regclass);


--
-- Name: warddetails_reject surid; Type: DEFAULT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.warddetails_reject ALTER COLUMN surid SET DEFAULT nextval('kaverimig.warddetails_reject_surid_seq'::regclass);


--
-- Name: app app_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: postgres
--

ALTER TABLE ONLY kaverimig.app
    ADD CONSTRAINT app_pkey PRIMARY KEY (surid);


--
-- Name: bannedproperties_reject bannedproperties_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.bannedproperties_reject
    ADD CONSTRAINT bannedproperties_reject_pkey PRIMARY KEY (surid);


--
-- Name: bannedpropertynumbers_reject bannedpropertynumbers_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.bannedpropertynumbers_reject
    ADD CONSTRAINT bannedpropertynumbers_reject_pkey PRIMARY KEY (surid);


--
-- Name: cc_applicationdetails_reject cc_applicationdetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.cc_applicationdetails_reject
    ADD CONSTRAINT cc_applicationdetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: cc_esignfilepath_reject cc_esignfilepath_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.cc_esignfilepath_reject
    ADD CONSTRAINT cc_esignfilepath_reject_pkey PRIMARY KEY (surid);


--
-- Name: cc_qrcodedetails_reject cc_qrcodedetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.cc_qrcodedetails_reject
    ADD CONSTRAINT cc_qrcodedetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: cc_signedfilepaths_reject cc_signedfilepaths_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.cc_signedfilepaths_reject
    ADD CONSTRAINT cc_signedfilepaths_reject_pkey PRIMARY KEY (surid);


--
-- Name: courtorders_reject courtorders_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.courtorders_reject
    ADD CONSTRAINT courtorders_reject_pkey PRIMARY KEY (surid);


--
-- Name: districtmaster_new_reject districtmaster_new_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.districtmaster_new_reject
    ADD CONSTRAINT districtmaster_new_reject_pkey PRIMARY KEY (surid);


--
-- Name: ec_applicationdetails_reject ec_applicationdetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ec_applicationdetails_reject
    ADD CONSTRAINT ec_applicationdetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: ec_esignfilepath_reject ec_esignfilepath_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ec_esignfilepath_reject
    ADD CONSTRAINT ec_esignfilepath_reject_pkey PRIMARY KEY (surid);


--
-- Name: ec_qrcodedetails_reject ec_qrcodedetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ec_qrcodedetails_reject
    ADD CONSTRAINT ec_qrcodedetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: ec_signedfilepaths_reject ec_signedfilepaths_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ec_signedfilepaths_reject
    ADD CONSTRAINT ec_signedfilepaths_reject_pkey PRIMARY KEY (surid);


--
-- Name: ecsearchdocumentnodetails_reject ecsearchdocumentnodetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ecsearchdocumentnodetails_reject
    ADD CONSTRAINT ecsearchdocumentnodetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: ecsearchpartydetails_reject ecsearchpartydetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ecsearchpartydetails_reject
    ADD CONSTRAINT ecsearchpartydetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: ecsearchpropertynodetails_reject ecsearchpropertynodetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ecsearchpropertynodetails_reject
    ADD CONSTRAINT ecsearchpropertynodetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: hoblimaster_reject hoblimaster_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.hoblimaster_reject
    ADD CONSTRAINT hoblimaster_reject_pkey PRIMARY KEY (surid);


--
-- Name: liabilitydetails_reject liabilitydetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.liabilitydetails_reject
    ADD CONSTRAINT liabilitydetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: liabilityonpropertydetails_reject liabilityonpropertydetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.liabilityonpropertydetails_reject
    ADD CONSTRAINT liabilityonpropertydetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: liabilitypropertymapped_reject liabilitypropertymapped_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.liabilitypropertymapped_reject
    ADD CONSTRAINT liabilitypropertymapped_reject_pkey PRIMARY KEY (surid);


SET default_tablespace = "Tablespace_Index";

--
-- Name: logdetails logdetails_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin; Tablespace: Tablespace_Index
--

ALTER TABLE ONLY kaverimig.logdetails
    ADD CONSTRAINT logdetails_pkey PRIMARY KEY (moment);


SET default_tablespace = '';

--
-- Name: openbuiltratedetail_reject openbuiltratedetail_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.openbuiltratedetail_reject
    ADD CONSTRAINT openbuiltratedetail_reject_pkey PRIMARY KEY (surid);


--
-- Name: partyinfo_reject partyinfo_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.partyinfo_reject
    ADD CONSTRAINT partyinfo_reject_pkey PRIMARY KEY (surid);


--
-- Name: jobstatus pk_jobid_jobstatus; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.jobstatus
    ADD CONSTRAINT pk_jobid_jobstatus PRIMARY KEY (jobid);


--
-- Name: ams_bankinstrumentnumberdetails_reject pk_rowid; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.ams_bankinstrumentnumberdetails_reject
    ADD CONSTRAINT pk_rowid PRIMARY KEY (row_id);


--
-- Name: propertymaster_reject propertymaster_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.propertymaster_reject
    ADD CONSTRAINT propertymaster_reject_pkey PRIMARY KEY (surid);


--
-- Name: propertyschedules_reject propertyschedules_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.propertyschedules_reject
    ADD CONSTRAINT propertyschedules_reject_pkey PRIMARY KEY (surid);


--
-- Name: rateagriculturaldetail_reject rateagriculturaldetail_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.rateagriculturaldetail_reject
    ADD CONSTRAINT rateagriculturaldetail_reject_pkey PRIMARY KEY (surid);


--
-- Name: roadmaster_new_reject roadmaster_new_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.roadmaster_new_reject
    ADD CONSTRAINT roadmaster_new_reject_pkey PRIMARY KEY (surid);


--
-- Name: sromaster_new_reject sromaster_new_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.sromaster_new_reject
    ADD CONSTRAINT sromaster_new_reject_pkey PRIMARY KEY (surid);


--
-- Name: surveynodetails_reject surveynodetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.surveynodetails_reject
    ADD CONSTRAINT surveynodetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: talukmaster_new_reject talukmaster_new_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.talukmaster_new_reject
    ADD CONSTRAINT talukmaster_new_reject_pkey PRIMARY KEY (surid);


--
-- Name: val_agriculturedetails_reject val_agriculturedetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_agriculturedetails_reject
    ADD CONSTRAINT val_agriculturedetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: val_annexuredetails_reject val_annexuredetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_annexuredetails_reject
    ADD CONSTRAINT val_annexuredetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: val_apartmentamenitydetails_reject val_apartmentamenitydetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_apartmentamenitydetails_reject
    ADD CONSTRAINT val_apartmentamenitydetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: val_constructionratedetails_reject val_constructionratedetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_constructionratedetails_reject
    ADD CONSTRAINT val_constructionratedetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: val_flatfloordetails_reject val_flatfloordetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_flatfloordetails_reject
    ADD CONSTRAINT val_flatfloordetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: val_flatratedetails_reject val_flatratedetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_flatratedetails_reject
    ADD CONSTRAINT val_flatratedetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: val_openbuiltvaluationdetails_reject val_openbuiltvaluationdetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_openbuiltvaluationdetails_reject
    ADD CONSTRAINT val_openbuiltvaluationdetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: val_parkingratedetails_reject val_parkingratedetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.val_parkingratedetails_reject
    ADD CONSTRAINT val_parkingratedetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: valuationdetails_reject valuationdetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.valuationdetails_reject
    ADD CONSTRAINT valuationdetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: villagemaster_reject villagemaster_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.villagemaster_reject
    ADD CONSTRAINT villagemaster_reject_pkey PRIMARY KEY (surid);


--
-- Name: warddetails_reject warddetails_reject_pkey; Type: CONSTRAINT; Schema: kaverimig; Owner: csgadmin
--

ALTER TABLE ONLY kaverimig.warddetails_reject
    ADD CONSTRAINT warddetails_reject_pkey PRIMARY KEY (surid);


--
-- Name: idx_bannedpropertynumber_orderid; Type: INDEX; Schema: kaverimig; Owner: csgadmin
--

CREATE INDEX idx_bannedpropertynumber_orderid ON kaverimig.bannedpropertynumbers_reject USING btree (orderid);


--
-- Name: idx_bannedpropertynumber_propertyid; Type: INDEX; Schema: kaverimig; Owner: csgadmin
--

CREATE INDEX idx_bannedpropertynumber_propertyid ON kaverimig.bannedpropertynumbers_reject USING btree (propertyid);


--
-- Name: idx_bannedpropertynumber_srocode; Type: INDEX; Schema: kaverimig; Owner: csgadmin
--

CREATE INDEX idx_bannedpropertynumber_srocode ON kaverimig.bannedpropertynumbers_reject USING btree (srocode);


--
-- Name: idx_bannedpropertynumbers_orderid; Type: INDEX; Schema: kaverimig; Owner: csgadmin
--

CREATE INDEX idx_bannedpropertynumbers_orderid ON kaverimig.bannedpropertynumbers_reject USING btree (currentpropertytypeid);


--
-- Name: SCHEMA kaverimig; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA kaverimig TO csgadmin;
GRANT ALL ON SCHEMA kaverimig TO csgmig;
GRANT USAGE ON SCHEMA kaverimig TO csgdeptuser;
GRANT USAGE ON SCHEMA kaverimig TO csgk2user WITH GRANT OPTION;
GRANT USAGE ON SCHEMA kaverimig TO bkpuser;
GRANT ALL ON SCHEMA kaverimig TO test_user;
GRANT ALL ON SCHEMA kaverimig TO csgkaverirwx;
GRANT ALL ON SCHEMA kaverimig TO sshuser;


--
-- Name: TABLE ams_bankinstrumentnumberdetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.ams_bankinstrumentnumberdetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ams_bankinstrumentnumberdetails_reject TO csgk2user;
GRANT ALL ON TABLE kaverimig.ams_bankinstrumentnumberdetails_reject TO csgmig;
GRANT SELECT,REFERENCES ON TABLE kaverimig.ams_bankinstrumentnumberdetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ams_bankinstrumentnumberdetails_reject TO csgkaverirwx;


--
-- Name: TABLE app; Type: ACL; Schema: kaverimig; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.app TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kaverimig.app TO csgk2user;
GRANT ALL ON TABLE kaverimig.app TO csgadmin;
GRANT ALL ON TABLE kaverimig.app TO csgmig;
GRANT SELECT,REFERENCES,TRIGGER ON TABLE kaverimig.app TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.app TO csgkaverirwx;
GRANT ALL ON TABLE kaverimig.app TO sumit WITH GRANT OPTION;


--
-- Name: SEQUENCE app_surid_seq; Type: ACL; Schema: kaverimig; Owner: postgres
--

GRANT ALL ON SEQUENCE kaverimig.app_surid_seq TO csgdeptuser;
GRANT SELECT ON SEQUENCE kaverimig.app_surid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaverimig.app_surid_seq TO csgadmin;
GRANT ALL ON SEQUENCE kaverimig.app_surid_seq TO csgmig;
GRANT ALL ON SEQUENCE kaverimig.app_surid_seq TO test_user;
GRANT ALL ON SEQUENCE kaverimig.app_surid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kaverimig.app_surid_seq TO sumit WITH GRANT OPTION;
GRANT SELECT,USAGE ON SEQUENCE kaverimig.app_surid_seq TO deptdba;
GRANT ALL ON SEQUENCE kaverimig.app_surid_seq TO csgcitizenuser;


--
-- Name: TABLE bannedproperties_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT SELECT,REFERENCES ON TABLE kaverimig.bannedproperties_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.bannedproperties_reject TO csgkaverirwx;
GRANT SELECT ON TABLE kaverimig.bannedproperties_reject TO csgk2user;


--
-- Name: SEQUENCE bannedproperties_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.bannedproperties_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.bannedproperties_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE bannedpropertynumbers_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.bannedpropertynumbers_reject TO csgreplica;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE kaverimig.bannedpropertynumbers_reject TO csgmig;
GRANT ALL ON TABLE kaverimig.bannedpropertynumbers_reject TO csgcitizenuser;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE kaverimig.bannedpropertynumbers_reject TO csgdeptuser;
GRANT SELECT,REFERENCES ON TABLE kaverimig.bannedpropertynumbers_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.bannedpropertynumbers_reject TO csgusermis;
GRANT SELECT,REFERENCES ON TABLE kaverimig.bannedpropertynumbers_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.bannedpropertynumbers_reject TO csgkaverirwx;


--
-- Name: SEQUENCE bannedpropertynumbers_reject_courtpropertynumberid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.bannedpropertynumbers_reject_courtpropertynumberid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kaverimig.bannedpropertynumbers_reject_courtpropertynumberid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.bannedpropertynumbers_reject_courtpropertynumberid_seq TO csgdeptuser;


--
-- Name: SEQUENCE bannedpropertynumbers_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.bannedpropertynumbers_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.bannedpropertynumbers_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE cc_applicationdetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.cc_applicationdetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.cc_applicationdetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.cc_applicationdetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.cc_applicationdetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.cc_applicationdetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE cc_applicationdetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.cc_applicationdetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.cc_applicationdetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE cc_esignfilepath_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.cc_esignfilepath_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.cc_esignfilepath_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.cc_esignfilepath_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.cc_esignfilepath_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.cc_esignfilepath_reject TO csgkaverirwx;


--
-- Name: SEQUENCE cc_esignfilepath_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.cc_esignfilepath_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.cc_esignfilepath_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE cc_qrcodedetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.cc_qrcodedetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.cc_qrcodedetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.cc_qrcodedetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.cc_qrcodedetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.cc_qrcodedetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE cc_qrcodedetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.cc_qrcodedetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.cc_qrcodedetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE cc_signedfilepaths_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.cc_signedfilepaths_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.cc_signedfilepaths_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.cc_signedfilepaths_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.cc_signedfilepaths_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.cc_signedfilepaths_reject TO csgkaverirwx;


--
-- Name: SEQUENCE cc_signedfilepaths_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.cc_signedfilepaths_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.cc_signedfilepaths_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE courtorders_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.courtorders_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.courtorders_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.courtorders_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.courtorders_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.courtorders_reject TO csgkaverirwx;


--
-- Name: SEQUENCE courtorders_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.courtorders_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.courtorders_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE districtmaster_new_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.districtmaster_new_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.districtmaster_new_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.districtmaster_new_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.districtmaster_new_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.districtmaster_new_reject TO csgkaverirwx;


--
-- Name: SEQUENCE districtmaster_new_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.districtmaster_new_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.districtmaster_new_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE ec_applicationdetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.ec_applicationdetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.ec_applicationdetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ec_applicationdetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.ec_applicationdetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ec_applicationdetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE ec_applicationdetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.ec_applicationdetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.ec_applicationdetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE ec_esignfilepath_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.ec_esignfilepath_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.ec_esignfilepath_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ec_esignfilepath_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.ec_esignfilepath_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ec_esignfilepath_reject TO csgkaverirwx;


--
-- Name: SEQUENCE ec_esignfilepath_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.ec_esignfilepath_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.ec_esignfilepath_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE ec_qrcodedetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.ec_qrcodedetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.ec_qrcodedetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ec_qrcodedetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.ec_qrcodedetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ec_qrcodedetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE ec_qrcodedetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.ec_qrcodedetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.ec_qrcodedetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE ec_signedfilepaths_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.ec_signedfilepaths_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.ec_signedfilepaths_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ec_signedfilepaths_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.ec_signedfilepaths_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ec_signedfilepaths_reject TO csgkaverirwx;


--
-- Name: SEQUENCE ec_signedfilepaths_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.ec_signedfilepaths_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.ec_signedfilepaths_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE ecsearchdocumentnodetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.ecsearchdocumentnodetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.ecsearchdocumentnodetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ecsearchdocumentnodetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.ecsearchdocumentnodetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ecsearchdocumentnodetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE ecsearchdocumentnodetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.ecsearchdocumentnodetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.ecsearchdocumentnodetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE ecsearchpartydetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.ecsearchpartydetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.ecsearchpartydetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ecsearchpartydetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.ecsearchpartydetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ecsearchpartydetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE ecsearchpartydetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.ecsearchpartydetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.ecsearchpartydetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE ecsearchpropertynodetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.ecsearchpropertynodetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.ecsearchpropertynodetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ecsearchpropertynodetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.ecsearchpropertynodetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.ecsearchpropertynodetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE ecsearchpropertynodetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.ecsearchpropertynodetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.ecsearchpropertynodetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE hoblimaster_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.hoblimaster_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.hoblimaster_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.hoblimaster_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.hoblimaster_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.hoblimaster_reject TO csgkaverirwx;


--
-- Name: SEQUENCE hoblimaster_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.hoblimaster_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.hoblimaster_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE jobstatus; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT TRUNCATE ON TABLE kaverimig.jobstatus TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.jobstatus TO csgmig WITH GRANT OPTION;
GRANT ALL ON TABLE kaverimig.jobstatus TO csgreplica;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.jobstatus TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.jobstatus TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.jobstatus TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.jobstatus TO csgkaverirwx;


--
-- Name: SEQUENCE jobstatus_jobid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.jobstatus_jobid_seq TO csgk2user;
GRANT ALL ON SEQUENCE kaverimig.jobstatus_jobid_seq TO csgkaverirwx;
GRANT ALL ON SEQUENCE kaverimig.jobstatus_jobid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.jobstatus_jobid_seq TO csgdeptuser;


--
-- Name: TABLE liabilitydetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.liabilitydetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.liabilitydetails_reject TO csgk2user;
GRANT ALL ON TABLE kaverimig.liabilitydetails_reject TO csgmig;
GRANT SELECT,REFERENCES ON TABLE kaverimig.liabilitydetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.liabilitydetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE liabilitydetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.liabilitydetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.liabilitydetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE liabilityonpropertydetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.liabilityonpropertydetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.liabilityonpropertydetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.liabilityonpropertydetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.liabilityonpropertydetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.liabilityonpropertydetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE liabilityonpropertydetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.liabilityonpropertydetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.liabilityonpropertydetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE liabilitypropertymapped_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.liabilitypropertymapped_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.liabilitypropertymapped_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.liabilitypropertymapped_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.liabilitypropertymapped_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.liabilitypropertymapped_reject TO csgkaverirwx;


--
-- Name: SEQUENCE liabilitypropertymapped_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.liabilitypropertymapped_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.liabilitypropertymapped_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE logdetails; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT TRUNCATE ON TABLE kaverimig.logdetails TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.logdetails TO csgmig WITH GRANT OPTION;
GRANT ALL ON TABLE kaverimig.logdetails TO csgreplica;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.logdetails TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.logdetails TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.logdetails TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.logdetails TO csgkaverirwx;


--
-- Name: TABLE openbuiltratedetail_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.openbuiltratedetail_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.openbuiltratedetail_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.openbuiltratedetail_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.openbuiltratedetail_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.openbuiltratedetail_reject TO csgkaverirwx;


--
-- Name: SEQUENCE openbuiltratedetail_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.openbuiltratedetail_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.openbuiltratedetail_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE partyinfo_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.partyinfo_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.partyinfo_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.partyinfo_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.partyinfo_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.partyinfo_reject TO csgkaverirwx;


--
-- Name: SEQUENCE partyinfo_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.partyinfo_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.partyinfo_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE propertymaster_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.propertymaster_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.propertymaster_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.propertymaster_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.propertymaster_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.propertymaster_reject TO csgkaverirwx;


--
-- Name: SEQUENCE propertymaster_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.propertymaster_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.propertymaster_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE propertyschedules_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.propertyschedules_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.propertyschedules_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.propertyschedules_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.propertyschedules_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.propertyschedules_reject TO csgkaverirwx;


--
-- Name: SEQUENCE propertyschedules_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.propertyschedules_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.propertyschedules_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE rateagriculturaldetail_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.rateagriculturaldetail_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.rateagriculturaldetail_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.rateagriculturaldetail_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.rateagriculturaldetail_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.rateagriculturaldetail_reject TO csgkaverirwx;


--
-- Name: SEQUENCE rateagriculturaldetail_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.rateagriculturaldetail_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.rateagriculturaldetail_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE roadmaster_new_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.roadmaster_new_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.roadmaster_new_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.roadmaster_new_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.roadmaster_new_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.roadmaster_new_reject TO csgkaverirwx;


--
-- Name: SEQUENCE roadmaster_new_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.roadmaster_new_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.roadmaster_new_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE sromaster_new_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.sromaster_new_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.sromaster_new_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.sromaster_new_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.sromaster_new_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.sromaster_new_reject TO csgkaverirwx;


--
-- Name: SEQUENCE sromaster_new_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.sromaster_new_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.sromaster_new_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE surveynodetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.surveynodetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.surveynodetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.surveynodetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.surveynodetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.surveynodetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE surveynodetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.surveynodetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.surveynodetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE talukmaster_new_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.talukmaster_new_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.talukmaster_new_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.talukmaster_new_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.talukmaster_new_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.talukmaster_new_reject TO csgkaverirwx;


--
-- Name: SEQUENCE talukmaster_new_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.talukmaster_new_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.talukmaster_new_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE val_agriculturedetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.val_agriculturedetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.val_agriculturedetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_agriculturedetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.val_agriculturedetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_agriculturedetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE val_agriculturedetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.val_agriculturedetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.val_agriculturedetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE val_annexuredetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.val_annexuredetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.val_annexuredetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_annexuredetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.val_annexuredetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_annexuredetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE val_annexuredetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.val_annexuredetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.val_annexuredetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE val_apartmentamenitydetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.val_apartmentamenitydetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.val_apartmentamenitydetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_apartmentamenitydetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.val_apartmentamenitydetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_apartmentamenitydetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE val_apartmentamenitydetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.val_apartmentamenitydetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.val_apartmentamenitydetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE val_constructionratedetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.val_constructionratedetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.val_constructionratedetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_constructionratedetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.val_constructionratedetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_constructionratedetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE val_constructionratedetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.val_constructionratedetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.val_constructionratedetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE val_flatfloordetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.val_flatfloordetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.val_flatfloordetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_flatfloordetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.val_flatfloordetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_flatfloordetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE val_flatfloordetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.val_flatfloordetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.val_flatfloordetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE val_flatratedetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.val_flatratedetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.val_flatratedetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_flatratedetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.val_flatratedetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_flatratedetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE val_flatratedetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.val_flatratedetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.val_flatratedetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE val_openbuiltvaluationdetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.val_openbuiltvaluationdetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.val_openbuiltvaluationdetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_openbuiltvaluationdetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.val_openbuiltvaluationdetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_openbuiltvaluationdetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE val_openbuiltvaluationdetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.val_openbuiltvaluationdetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.val_openbuiltvaluationdetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE val_parkingratedetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.val_parkingratedetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.val_parkingratedetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_parkingratedetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.val_parkingratedetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.val_parkingratedetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE val_parkingratedetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.val_parkingratedetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.val_parkingratedetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE valuationdetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.valuationdetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.valuationdetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.valuationdetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.valuationdetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.valuationdetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE valuationdetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.valuationdetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.valuationdetails_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE villagemaster_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.villagemaster_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.villagemaster_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.villagemaster_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.villagemaster_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.villagemaster_reject TO csgkaverirwx;


--
-- Name: SEQUENCE villagemaster_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.villagemaster_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.villagemaster_reject_surid_seq TO csgdeptuser;


--
-- Name: TABLE warddetails_reject; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON TABLE kaverimig.warddetails_reject TO csgmig;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLE kaverimig.warddetails_reject TO csgdeptuser;
GRANT SELECT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.warddetails_reject TO csgk2user;
GRANT SELECT,REFERENCES ON TABLE kaverimig.warddetails_reject TO test_user;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLE kaverimig.warddetails_reject TO csgkaverirwx;


--
-- Name: SEQUENCE warddetails_reject_surid_seq; Type: ACL; Schema: kaverimig; Owner: csgadmin
--

GRANT ALL ON SEQUENCE kaverimig.warddetails_reject_surid_seq TO csgcitizenuser;
GRANT ALL ON SEQUENCE kaverimig.warddetails_reject_surid_seq TO csgdeptuser;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: kaverimig; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON SEQUENCES  TO csgdeptuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON SEQUENCES  TO csgadmin;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON SEQUENCES  TO csgmig;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON SEQUENCES  TO test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON SEQUENCES  TO csgkaverirwx;


--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: kaverimig; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON TYPES  TO csgadmin;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON TYPES  TO test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON TYPES  TO csgkaverirwx;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: kaverimig; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON FUNCTIONS  TO csgadmin;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON FUNCTIONS  TO test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON FUNCTIONS  TO csgkaverirwx;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: kaverimig; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,UPDATE ON TABLES  TO csgdeptuser;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT SELECT ON TABLES  TO csgk2user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON TABLES  TO csgadmin;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT ALL ON TABLES  TO csgmig;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT SELECT,REFERENCES,TRIGGER ON TABLES  TO test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA kaverimig GRANT SELECT,INSERT,REFERENCES,TRIGGER,UPDATE ON TABLES  TO csgkaverirwx;


--
-- PostgreSQL database dump complete
--

