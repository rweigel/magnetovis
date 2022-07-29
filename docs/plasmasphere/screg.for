C From HOFFMAN@NSSDCA.GSFC.NASA.GOV Tue Jun  7 15:13:46 1994
C Return-Path: <HOFFMAN@NSSDCA.GSFC.NASA.GOV>
C Received: from NSSDCA.GSFC.NASA.GOV by sscdev1.stx.com.stx.com (4.1/SMI-4.1)
C       id AA02063; Tue, 7 Jun 94 15:13:41 EDT
C Date: Tue, 7 Jun 1994 15:15:08 -0400 (EDT)
C From: "Douglas J. Hoffman (301) 441-4176" <HOFFMAN@NSSDCA.GSFC.NASA.GOV>
C To: doug@sscdev1.stx.com
C Message-Id: <940607151508.224074d1@NSSDCA.GSFC.NASA.GOV>
C Status: R
C 
C From: ISTP::PEREDO       "MAURICIO PEREDO, Hughes STX/ISTP-SPOF, 
C 301/286-1526" 11-APR-1994 14:45:33.73
C To:   NCF::HOFFMAN,NCF::SARDI
C CC:   NCF::MCGUIRE,PEREDO
C Subj: source code for screg.for
C
C************************************************************************
C                                                                       *
C SUBROUTINE:   SCREG.FOR                                               *
C               CREATED: March 31, 1994                                 *
C               PROJECTS: SPOF & SSC                                    *
C                                                                       *
c                                                                       *
C  ENGLISH NAME: Magnetospheric (Spacecraft) Regions for SSC Programs   *
C  LANGUAGE: FORTRAN77                                                  *
C                                                                       *
C                                                                       *
C  CALLING SEQUENCE:  CALL SCREG(GEI,IYEAR,IDAY,HR,PSW,BZIMF,IREG)      *
C                                                                       *
C                                                                       *
C  PURPOSE:     To identify the magnetospheric region occupied by       *
C               a given spacecraft                                      *
C                                                                       *
C  METHOD:      The subroutine receives the spacecraft position along   *
C               with date and time (needed for coordinate conversions)  *
C               Calls are then made to subsidiary routines to determine *
C               if the s/c is "inside/outside" modeled boundaries.      *
C               The region occupied by the s/c is identified by the     *
C               integer parameter IREG.                                 *
C                                                                       *
C                                                                       *
C  INPUT/OUTPUT                                                         *
C                                                                       *
C       GEI = 3 COMPONENT VECTOR WITH S/C POSITION IN GEI COORDINATES   *
C       IYEAR = integer 4 digit year (i.e. 1979)                        *
C       IDAY = integer day of year (i.e. 250)                           *
C       HR = floating hour of day (i.e. 15.5) - UNIVERSAL TIME -        *
C       PSW = SOLAR WIND DYNAMIC PRESSURE FOR INPUT DATE/TIME           *
C       BZIMF = Bz component (GSM coordinates) of the IMF for input     *
C               date/time                                               *
C                                                                       *
C  OUTPUT                                                               *
C                                                                       *
C       IREG =  INDEX IDENTIFYING THE REGION OCCUPIED BY S/C            *
C                                                                       *
C                                                                       *
C  CALLS:                                                               *
C                                                                       *
C       SUNPOS(*)                                                       *
C                                                                       *
C       GEIGSE(*)                                                       *
C          ... MLTPLY(*)                                                *
C                                                                       *
C       GEIGSM(*)                                                       *
c          ... GEOGEI(*)                                                *
C          ... MLTPLY(*)                                                *
C                                                                       *
C       GEISM(*)                                                        *
C          ... GEOGEI(*)                                                *
C          ... MLTPLY(*)                                                *
C                                                                       *
C       ABER(*)                                                         *
C                                                                       *
C       BSMP(*)                                                         *
C                                                                       *
C       BLAYERS(*)                                                      *
C                                                                       *
C       ZNEUT94(*)                                                      *
C                                                                       *
C       PSPH_V2(*)                                                      *
C         ... LOGDEN_V2(*)                                              *
C         ... CARSPH_V2(*)                                              *
C                                                                       *
C       YROUND(*)                                                       *
C                                                                       *
C                                                                       *
C  ERROR HANDLING:                                                      *
C                                                                       *
C                                                                       *
C  DESIGN AND CODING:   MAURICIO PEREDO                                 *
C                       Hughes STX Corporation                          *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       ISTP/GGS SPOF                                   *
C                       Code 695                                        *
C                                                                       *
C   ADDRESS:            MAURICIO PEREDO                                 *
C                       CODE 695                                        *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       GREENBELT, MARYLAND 20771                       *
C                       USA                                             *
C                       PHONE   (301) 286-1526                          *
c                       FAX     (301) 286-1683                          *
C                       E-MAIL: ISTP::PEREDO                            *
c                               peredo@istp1.gsfc.nasa.gov              *
C                                                                       *
C                                                                       *
C  MODIFICATIONS/UPDATES:                                               *
C                                                                       *
c       Adapted from the routine SSCREG_V2 used in V.2.0 - 2.2 of the.  *
c       SSC. Changes relative to SSCREG_V2 include: (1) mapped regions  *
c       are now computed via a separate routine MAPREG, (2) The         *
c       Fairfield neutral sheet model has been replaced with the        *
c       current sheet model proposed for the new generation of          *
c       Tsyganenko models under development by the GSFC modeling        *
c       group; a new subroutine ZNEUT94.FOR has been created for        *
c       that model, (3) the Sibeck magnetopause model has been          *
c       "updated" to use the new version which uses a bivariate         *
C       fit depending on solar wind pressure AND IMF-Bz; the routine    *
C       BSMP_V2.FOR has been modified to use the new magnetopause       *
C       definition, and has been renamed BSMP.FOR.                      *
C                                                                       *
C********1*********2*********3*********4*********5*********6*********7***
C
C
C
      SUBROUTINE SCREG(GEI,IYEAR,IDAY,HR,PSW,BZIMF,IREG)
C
        IMPLICIT NONE
        INCLUDE 'parms.inc'
C
c        real GEI(3),GSE(3),GSM(3),SM(3),S(3),AGSE(3), AGSM(3)
        DOUBLE PRECISION GEI(3),GSE(3),GSM(3),SM(3),S(3),AGSE(3),AGSM(3)
c        real PSW,BZIMF
        DOUBLE PRECISION PSW,BZIMF
c        real TANTA,DBL,RR,DELR
c        real HR,GMST,SLONG,SRASN,SDEC,SEPS,CEPS,RSAT
        DOUBLE PRECISION RMP,DNS,SINTA,COSTA
        DOUBLE PRECISION TANTA,DBL,RR,DELR
        DOUBLE PRECISION HR,GMST,SLONG,SRASN,SDEC,SEPS,CEPS,RSAT
        INTEGER IREG,IMAP,I,IYEAR,IDAY

        INTEGER JYRND
        INTEGER YROUND
C
C       INITIALIZATION
C
        JYRND = YROUND(IYEAR,IDAY,HR)
        IREG = NONE
        IMAP = NONE
C
C       CHECK THAT INPUT POINT IS OUTSIDE THE EARTH -- ELSE ABORT
C
c        RSAT = SQRT( GEI(1)*GEI(1) + GEI(2)*GEI(2) + GEI(3)*GEI(3) )
        RSAT = DSQRT( GEI(1)*GEI(1) + GEI(2)*GEI(2) + GEI(3)*GEI(3) )
C           print *,'in screg gei, rsat  = ',gei, rsat
C
C Too many conversions on the code make this test difficult to pass
C and we do not need this much precision.
C 10/95 EPM
        IF (RSAT.LT.0.9) THEN
C           WRITE(*,*) 'IMPROPER INPUT FOR SSCREG - ABORT'
           RETURN
C
        ELSE
C
           DO 10 I=1,3
              GSE(I) = 0.
              GSM(I) = 0.
              SM(I)  = 0.
10         CONTINUE
C
C       Compute aparent position of the Sun and necessary angles
C       to carry out conversions to GSE,GSM and SM coordinates
C
          CALL SUNPOS(IYEAR,IDAY,HR,GMST,SLONG,SRASN,SDEC,SEPS,CEPS,S)
          CALL GEIGSE(GEI,S,SEPS,CEPS,GSE)
C
C       Check s/c position v.s. Bow Shock and Magnetopause boundaries
C
c           print *,'in screg gei = ',gei
           CALL ABER(GSE,AGSE)
           CALL BSMP(AGSE,PSW,BZIMF,IREG,RMP)
C
C       If IREG returns as Interplanetary Medium, Dayside Magnetosheath
C       or Nightside Magnetosheath, then region has been identified.
C       Alternatively, we proceed to check other regions.
C
           IF ((IREG.EQ.INTMED).OR.(IREG.EQ.DMSH).OR.
     1             (IREG.EQ.NMSH)) RETURN
C
C       If we get here, s/c is inside magnetopause, and we need GSM and
C       SM coordinates to further establish region occupied by s/c.
c       Note that BSMP has set IREG to either DMSPH or NMSPH according
c       to whether the s/c is in the day/nightside magnetosphere; below
c       we check for other magnetospheric regions and if the s/c is not
c       in any of them, then the DMSPH or NMSPH designation is already
c       in place.
C
           CALL GEIGSM(GEI,S,GMST,JYRND,GSM)
           CALL GEISM(GEI,S,GMST,JYRND,SM)
c
C       Extract sine of the dipole tilt angle from GSM and SM components
c       and compute cosine and tangent; these values will be needed for
c       the computation of the distance from the current sheet
C
        SINTA = (GSM(1)*SM(3)-SM(1)*GSM(3)) /
     +          (GSM(1)*GSM(1)+GSM(3)*GSM(3))
c        COSTA = SQRT(1.-SINTA*SINTA)
        COSTA = DSQRT(1.-SINTA*SINTA)
        TANTA = SINTA/COSTA
C
C       If the s/c is in the nightside (defined as X-GSM < 0) then
c       we compute the distance from the current sheet surface. We
c       use aberrated GSM coordinates to determine if the s/c is
c       in the LLBL, HLBL or any of the tail regions.
c
        CALL ABER(GSM,AGSM)
c
        IF (GSM(1).LT.0.0) THEN
           CALL ZNEUT94(AGSM,SINTA,COSTA,TANTA,DNS)
c
c       Now compute the thickness of the HLBL and LLBL (call it DBL) 
c       at the same X-AGSM as the s/c.
c
           CALL BLAYERS(AGSM,DBL)
c
c       Check to see if s/c in HLBL or LLBL -- the dividing line from
c       LLBL to HLBL is when the distance to from the current sheet
c       is 3 Re (i.e the same distance used as the thickness of the
c       Plasma Sheet, which is meant to include PS and PSBL).
c
c           RR = SQRT( AGSM(2)*AGSM(2) + AGSM(3)*AGSM(3) )
           RR = DSQRT( AGSM(2)*AGSM(2) + AGSM(3)*AGSM(3) )
           DELR = RMP - RR
c
           IF (DELR.LT.DBL) THEN
c              IF (DNS.LE.3.) THEN 
c             IF (DNS.LE.3.) THEN     RTB 2/99
              IF ((ABS(DNS)).LE.3.) THEN
                 IREG = LLBL
                 RETURN
              ELSE 
                 IREG = HLBL
                 RETURN
              ENDIF
           ELSE
C               If we are tailward of the Hinging Distance (RH=8 Re) we check to
c               see if the spacecraft is in the tail regions PSHEET or LOBE
              IF (AGSM(1).LE.-8.) THEN
c                 IF (DNS.LE.3.) THEN 
c                 IF (DNS.LE.3.) THEN   RTB 2/99
                IF ((ABS(DNS)).LE.3.) THEN
                    IREG = PSHEET
                    RETURN
                 ELSE
                    IREG = LOBE
                    RETURN
                 ENDIF
              ENDIF
           ENDIF
        ENDIF
c
c       We reach this point if the s/c was not in any of the regions HLBL, LLBL,
c       PSHEET or LOBE; we check to see if it is inside the plasmasphere and if
c       not by process of elimination it must be in the day/night magnetosphere.
c
        CALL PSPH_V2(SM,IREG)
c
        ENDIF
C
        RETURN
        END
C



C************************************************************************
C                                                                       *
C SUBROUTINE: BSMP.FOR   CREATED: JUNE 17, 1991   PROJECT: NSSDC/SSC    *
C                                                                       *
C  ENGLISH NAME: Bow Shock - Magnetopause                               *
C  LANGUAGE: FORTRAN77                                                  *
C                                                                       *
C  CALLING SEQUENCE:    CALL BSMP(AGSE,PSW,BZIMF,IREG,RMP)              *
C                                                                       *
C                                                                       *
C  PURPOSE:     To determine if spacecraft is inside/outside bow shock  *
C               and inside/outside magnetopause.                        *
C                                                                       *
C  METHOD:      The subroutine receives the spacecraft position in      *
C               aberrated (Cartesian) GSE coordinates, the solar wind   *
c               dynamic pressure, and the IMF-Bz component.             *
C               The magnetopause boundary is determined according to    *
C               the model of Roelof and Sibeck, "Magnetopause shape as  *
c               a bivariate function of Interplanetary Magnetic Field   *
c               Bz and solar wind dynamic pressure [JGR, 98, 21421,     *
c               1993] while the bow shock boundary is a modified        *
c               version of the Fairfield model [JGR, 76, 6700, 1971].   *
c               The modification includes displacement of the bow shock *
C               along the (aberrated) X axis so that the ratio of the   *
C               distance to the nose of the bow shock to the distance   *
C               to the nose of the magnetopause (Roelog & Sibeck model) *
C               remains fixed at 1.3.  This feature allows modeling     *
C               of the compression of the dayside magnetosphere at      *
C               times of high solar wind pressure.  Since Sibeck's      *
C               magnetopause is based on data out to approximately      *
C               X=-40, a cylinder has been patched to Sibeck's          *
C               magnetopause for X <= XCYL and XCYL has been            *
C               initially set to XCYL = -40, this has been structured   *
C               so that a single change to the value of XCYL permits    *
C               modification of the point at which the cylinder is      *
C               joined to the "elipsoidal" magnetopause.                *
C                                                                       *
C                                                                       *
C       SIBECK'S MP FOLLOWS FROM:                                       *
C                                                                       *
C       Z^2 + Y^2 + S1 X^2 + S2 X + S3 = 0                              *
C                                                                       *
C       where                                                           *
C                                                                       *
C       S1, S2 and S3 are constants corresponding to the best fit       *
C       obtained by Sibeck et. al.  Their values are computed using     *
c       a segment of code provided to M. Peredo by D. Sibeck            *
C                                                                       *
C                                                                       *
C       FAIRFIELD'S BS FOLLOWS FROM:                                    *
C                                                                       *
C       Y^2 + A X Y + B X^2 + C Y + D X + E = 0,                        *
C                                                                       *
C       where                                                           *
C                                                                       *
C       the constants for the best fit are:                             *
C                                                                       *
C       A = 0.0296                                                      *
C       B = -0.0381                                                     *
C       C = -1.280                                                      *
C       D = 45.644                                                      *
C       E = -652.10                                                     *
C                                                                       *
C       Fairfield's model is modified by replacing X -> (X - X0)        *
C       with X0 evaluated so that at Y = 0 (the nose) there is a        *
C       constant ratio of 0.3 between de distance MP-BS and MP          *
C       (in other words, the distance to the nose of the bow shock is   *
C       1.3 times the distance to the nose of Sibeck's magnetopause)    *
C                                                                       * 
C       Computation of X0 yields:                                       *
C                                                                       *
C       X0 = {1.3*[-S2 + SQRT(S2^2 - 4*S1*S3)]/(2*S1) } - 14.4612       *
C                                                                       *
C                                                                       *
C       Thus, the expression used for the bow shock has the form:       *
C                                                                       *
C       R^2 + A (X - X0) R + B (X - X0)^2 + C R + D (X - X0) + E = 0,   *
C                                                                       *
C       where we have assumed a rotation about the aberrated X-axis     *
C       to generate a 3D surface; thus R^2 = Y^2 + Z^2                  *
C                                                                       *
C                                                                       *
C  INPUT/OUTPUT                                                         *
C                                                                       *
C       AGSE = 3 COMPONENT VECTOR WITH S/C POSITION IN AGSE COORDINATES *
C       PSW = SOLAR WIND DYNAMIC PRESSURE FOR INPUT DATE/TIME           *
c       BZIMP = Interplanetary Magnetic Field Bz for input date/time    *
C                                                                       *
C  OUTPUT                                                               *
C                                                                       *
C       IREG = INDEX IDENTIFYING THE REGION OCCUPIED BY S/C             *
C       RMP =   Radius of the magnetopause at X of s/c to be used       *
C               by TAIL to determine if s/c in mantle or not            *
C                                                                       *
C                                                                       *
C  CALLS:                                                               *
C               NONE                                                    *
C                                                                       *
C                                                                       *
C                                                                       *
C  ERROR HANDLING:                                                      *
C                                                                       *
C                                                                       *
C  DESIGN AND CODING:   MAURICIO PEREDO                                 *
C                       Hughes STX Corporation                          *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       ISTP/GGS SPOF                                   *
C                       Code 695                                        *
C                                                                       *
C   ADDRESS:            MAURICIO PEREDO                                 *
C                       CODE 695                                        *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       GREENBELT, MARYLAND 20771                       *
C                       USA                                             *
C                       PHONE   (301) 286-1526                          *
c                       FAX     (301) 286-1683                          *
C                       E-MAIL: ISTP::PEREDO                            *
c                               peredo@istp1.gsfc.nasa.gov              *
C                                                                       *
C                                                                       *
C  MODIFICATIONS/UPDATES:                                               *
C                                                                       *
C                                                                       *
C********1*********2*********3*********4*********5*********6*********7***
C
C
C
      SUBROUTINE BSMP(AGSE,PSW,BZIMF,IREG,RMP)
C
        IMPLICIT NONE
        INCLUDE 'parms.inc'
C
c        real AGSE(3)
c        real PSW,BZIMF,S1,S2,S3,X,X2,R2,R,XCYL,
        DOUBLE PRECISION AGSE(3)
c	real PSW,BZIMF,S1,S2,S3,X,X2,R2,R,XCYL,
	DOUBLE PRECISION PSW,BZIMF,S1,S2,S3,X,X2,R2,R,XCYL,
     x     POLYMP,RMP,A,B,C,D,E,X0,DX,POLYBS,RCYL,SS,SS2,TT,UU,
     x     TEMP,XMPNOSE
        INTEGER IREG
C
C
C       Define XCYL =   value of X at which a cylinder is patched onto
C                       Roelof and Sibeck's magnetopause.
C
c        print *, 'in screg....'
        XCYL = -40.
C
C       Compute magnetopause polynomial to test inside/outside location
C       POLYMP = Z^2 + Y^2 + S1 X^2 + S2 X + S3
C       For X beyond (XCYL = -45 Re, a cylinder is patched on to the
C       magnetopause model of Sibeck and POLYMP is defined as R - RCYL
C       where RCYL is the radius of the cylinder (corresponding to the
C       radius of Sibeck's magnetopause at X = XCYL).
C       POLYMP = positive ==> outside --- POLYMP = negative ==> inside
C       We compute the constants in polynomial using algorithm provided by
c       D. Sibeck.
c
        SS = BZIMF + 0.1635
        SS2 = SS*SS
        TT = PSW/2.088
        UU = LOG(TT)
c
      S1=0.171*TT**(-0.474-0.616*UU+0.023*SS)*exp(-0.043*SS+0.0391*SS2)
      S2=18.80*TT**(-0.120-0.030*UU+0.036*SS)*exp(-0.037*SS+0.0002*SS2)
      S3=-220.8*TT**(-0.290-0.110*UU+0.018*SS)*exp(-0.012*SS+0.0017*SS2)
C
        X = AGSE(1)
        X2 = X*X
        R2 = AGSE(2)*AGSE(2) + AGSE(3)*AGSE(3)
c        R = SQRT(R2)
        R = DSQRT(R2)
C
C
        IF (X.GE.-45.0) THEN
           POLYMP = R2 + S1*X2 + S2*X + S3
C
C          Compute MP radius at s/c X (only if argument of sqrt is positive)
C
           IF ( (R2-POLYMP).GE.0.) THEN
c              RMP = SQRT(R2 - POLYMP)
              RMP = DSQRT(R2 - POLYMP)
           ELSE
              RMP = 0.
           ENDIF
C
        ELSE
C
C          Compute RCYL = radius at X = XCYL and set RMP = RCYL
C
c           RCYL = SQRT(-S1*XCYL*XCYL-S2*XCYL-S3)
           RCYL = DSQRT(-S1*XCYL*XCYL-S2*XCYL-S3)
           RMP = RCYL
           POLYMP = R - RCYL
        ENDIF
c        print *, 'in screg. rmp = ',rmp
C
C===============================================================================
C       Compute bow shock polynomial to test inside/outside location
C       POLYBS = R^2 + A (X - X0) R + B (X - X0)^2 + C R + D (X - X0) + E
C       (Fairfield, 1971)
C       POLYBS = positive ==> outside --- POLYBS = negative ==> inside
C       Define constants in polynomial
        A = 0.0296
        B = -0.0381
        C = -1.280
        D = 45.644
        E = -652.10
c
c       X0 is defined in terms of the paramters of the Roelof and Sibeck
c       magnetopause so that a constant ration of 1.3 exists between the
c       bow shock and magnetopause standoff distances. We compute XMPNOSE
c       the magnetopause standoff distance and then define X0 in terms of
c       XMPNOSE
c
        TEMP = S2*S2 - 4.*S1*S3
        IF (TEMP.GE.0.) THEN
c           XMPNOSE = (1.3*0.5*(-S2+SQRT(TEMP))/S1 ) - 14.4612
           XMPNOSE = (1.3*0.5*(-S2+DSQRT(TEMP))/S1 ) - 14.4612
        ELSE
c       If we get here, the argument of the square root is negative and
c       we have a problem -- print and error message
           write(*,*) 'Error in SQRT getting MP standoff distance'
        ENDIF
c
c        print *, 'in screg. x, x0 = ',x, x0
C       RCJ 03/2011   I think this is wrong. x0 should be xmpnose. See
C			documentation above.
C        DX = X - X0
        DX = X - XMPNOSE
C
        POLYBS = R2 + A*DX*R + B*DX*DX + C*R + D*DX + E
c	print *,'r,agse(1)= ',r,agse(1)
C
C       Assign values to IREG according to polynomial signs.
c       Note that for a point inside the magnetosphere we assign
c       either DMSPH or NMSPH based on sign of X-AGSE component.
c       This information is used back in SCREG.FOR since all positions
c       that are not in one of the other regions checked, are by default
c       in either DMSPH or NMSPH.
C
        IF (POLYBS.GT.0.) THEN
           IREG = INTMED
        ELSEIF ( (POLYBS.LE.0.).AND.(POLYMP.GT.0.) ) THEN
           IF (AGSE(1).GE.0.) THEN
              IREG = DMSH
           ELSEIF (AGSE(1).LT.0.) THEN
              IREG = NMSH
           ENDIF
        ELSEIF (POLYMP.LE.0.) THEN
           IF (AGSE(1).GE.0.) THEN
              IREG = DMSPH
           ELSEIF (AGSE(1).LT.0.) THEN
              IREG = NMSPH
           ENDIF
        ENDIF
C
c        print *, 'in screg.polybs,agse(1) = ',polybs,agse(1)
c        print *, 'in screg.intmed,ireg = ',intmed,ireg
        RETURN
        END



C************************************************************************
C                                                                       *
C SUBROUTINE:   ZNEUT94.FOR                                             *
C               CREATED: JUNE 19, 1991   PROJECT: NSSDC/SSC             *
C                                                                       *
C  ENGLISH NAME: Distance to the Neutral Sheet                          *
C  LANGUAGE: FORTRAN77                                                  *
C                                                                       *
C                                                                       *
C  CALLING SEQUENCE:    CALL ZNEUT94(AGSM,SINTA,COSTA,TANTA,DNS)        *
C                                                                       *
C                                                                       *
C  PURPOSE:     To compute the distance (vertically) between the        *
C               s/c position and the model neutral sheet.               *
C                                                                       *
C  METHOD:      The subroutine receives the spacecraft position in      *
C               aberrated (Cartesian) GSM coordinates. For Version 2.2  *
c               of the SSC, the Fairfield neutral sheet model [JGR, 85, *
c               775, 1980] has been replaced because it is not valid    *
c               over the entire range in X-GSM where we wish to use it. *
c               In place of Fairfield's model we use a model for the    *
c               current sheet surface proposed by N. A. Tsyganenko      *
c               to be used in the developement of the next generation   *
c               of empirical models (Tsyganenko and Stern, Spring 1994  *
c               AGU; a formal reference will be added here later)       *
C                                                                       *
C  INPUT/OUTPUT                                                         *
C                                                                       *
C       GSM =   3 COMPONENT VECTOR WITH S/C POSITION IN Aberrated-GSM   *
c               COORDINATES                                             *
C       SINTA  = Sine of the tile angle                                 *
C       COSTA  = Cosine of the tile angle                               *
C       TANTA  = Tangent of the tile angle                              *
C                                                                       *
C  OUTPUT                                                               *
C                                                                       *
C       DNS = DISTANCE TO THE NEUTRAL SHEET, I.E. Z(S/C) -Z(NS)         *
C                                                                       *
C  CALLS:                                                               *
C               NONE                                                    *
C                                                                       *
C                                                                       *
C                                                                       *
C  DESIGN AND CODING:   MAURICIO PEREDO                                 *
C                       Hughes STX Corporation                          *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       ISTP/GGS SPOF                                   *
C                       Code 695                                        *
C                                                                       *
C   ADDRESS:            MAURICIO PEREDO                                 *
C                       CODE 695                                        *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       GREENBELT, MARYLAND 20771                       *
C                       USA                                             *
C                       PHONE   (301) 286-1526                          *
c                       FAX     (301) 286-1683                          *
C                       E-MAIL: ISTP::PEREDO                            *
c                               peredo@istp1.gsfc.nasa.gov              *
C                                                                       *
C                                                                       *
C  MODIFICATIONS/UPDATES:                                               *
C                                                                       *
C                                                                       *
C********1*********2*********3*********4*********5*********6*********7***
C
C
C
      SUBROUTINE ZNEUT94(AGSM,SINTA,COSTA,TANTA,DNS)
C
        IMPLICIT NONE
        INCLUDE 'parms.inc'
C
c        double precision AGSM(3)
c        real SINTA,COSTA,TANTA,DNS,RH,DELX,G,LY,
        DOUBLE PRECISION AGSM(3),SINTA,COSTA,TANTA,DNS,RH,DELX,G,LY,
     1     LY4,Y4,T1,T2,T3,T4,T5,ZNS
C
C       Define coefficients for currrent sheet model
c
        RH=8.
        DELX=4.
        G=10.
        LY=10.
        LY4=LY*LY*LY*LY
C
C       Compute neutral sheet position and difference Z(s/c) - Z(ns)
C
        T1=RH*COSTA
        T2=(AGSM(1)-T1)*(AGSM(1)-T1)
        T3=(AGSM(1)+T1)*(AGSM(1)+T1)
        T4=DELX*DELX*COSTA*COSTA
        Y4=AGSM(2)*AGSM(2)*AGSM(2)*AGSM(2)
        T5=G*SINTA*Y4/(Y4+LY4)
c
c       The current sheet position is computed from the
c       formula:
c
c       ZNS=0.5*tan(tilt)*{ sqrt[(x-RH*cos(tilt))^2 + (DELX cos(tilt))^2]
c                         - sqrt[(x+RH*cos(tilt))^2 + (DELX cos(tilt))^2]}
c           - G*sin(tilt) * y^4 / (y^4 + LY^4)
c
c        ZNS = 0.5 * TANTA * ( SQRT(T2 + T4) - SQRT(T3 + T4) ) - T5
        ZNS = 0.5 * TANTA * ( DSQRT(T2 + T4) - DSQRT(T3 + T4) ) - T5
C
        DNS = AGSM(3) - ZNS
C
        RETURN
        END




C************************************************************************
C                                                                       *
C SUBROUTINE: PSPH_V2.FOR   CREATED: MARCH 3, 1992   PROJECT: NSSDC/SSC *
C                                                                       *
C  ENGLISH NAME: Plasmasphere                                           *
C  LANGUAGE: FORTRAN77                                                  *
C                                                                       *
C                                                                       *
C  CALLING SEQUENCE:    CALL PSPH_V2(SM,IREG)                           *
C                                                                       *
C                                                                       *
C  PURPOSE:     To determine if satellite is in the plasmasphere        *
C               or in the plasmapause.                                  *
C                                                                       *
C  METHOD:      The subroutine receives the spacecraft position in      *
C               cartesian SM coordinates and returns the region         *
C               identifier IREG which is modified only if the s/c       *
C               is inside the plasmasphere (day or night).  The         *
C               boundary (plasmapause) is defined from the model        *
C               of Gallagher, Craven and Comfort [Adv. Space Res.       *
C               Vol. 8, pp 15-24, 1988].                                *
c               The model consists of an empirical formula for the      *
C               plasma density (n) as a function of L=McIlwain's        *
C               L-parameter, MLT=magnetic local time, h(L,lamda)=height *
C               above Earth's surface, NOTE: BY TRIAL AND ERROR, I HAVE *
C               FOUND THAT h SHOULD BE IN KM where lamda=geomagnetic    *
C               latitude.  Free parameters in the model were determined *
C               by fitting to DE 1 RIMS observations. Use involves a    *
c               call to subroutine logden with position in spherical    *
C               SM coordinates which returns the value of               *
C               log(n)=log(plasma density) (n in cm-3). The boundary    *
C               is identified by the level log(n) = 1.5 with            *
C               log(n) > 1.5 representing a point inside the plasma-    *
C               sphere.                                                 *
C               Several further notes must be emphasized about the      *
C               use of the model in practice. Because of the dependence *
C               on L = R/cos^2(mlat), we must clearly impose a limit    *
C               on mlat to avoid overflow errors. This however is       *
C               trivial since at high magnetic latitudes one is         *
C               clearly outside the plasmasphere. Another related       *
C               point is that the variation of log(n) in the model      *
C               with respect to radial distance takes a very sharp      *
C               dip (toward negative values) for small distances --     *
C               clearly however, the model is not valid at very low     *
C               altitudes when one is in the ionosphere. To avoid       *
C               such conflicts, we DO NOT check for presence in the     *
C               plasmasphere for points with R < 1.05 Re (that level    *
C               corresponds to an altitude of the order of 300 km)      *
C               At the R=1.05 surface, we find that the plasmapause     *
C               boundary (defined by the above criterion log(n)=1.5     *
C               varies with MLT, but from checks at various MLT values  *
C               we find that a point will clearly lie outside the       *
C               plasmapause if THETA <= 28 or THETA >= 152. Thus        *
C               if THETA satisfies either of these conditions, we       *
C               exit without computing log(n) and the region identifier *
C               is not changed (similarly if R<1.05 Re)                 *
C               Finally, if R is sufficiently large, the point is       *
C               clearly outside, and there is no sense in computing     *
C               log(n). We choose R = 6 Re for this criterion.          *
C                                                                       *
C                                                                       *
C  INPUT/OUTPUT                                                         *
C                                                                       *
C       SM  = 3 COMPONENT VECTOR WITH S/C POSITION IN SM COORDINATES    *
C                                                                       *
C  OUTPUT                                                               *
C                                                                       *
C       IREG =  INDEX IDENTIFYING THE REGION OCCUPIED BY S/C            *
C                                                                       *
C  CALLS:                                                               *
C               CARSPH_V2                                               *
C               LOGDEN_V2                                               *
C                                                                       *
C                                                                       *
C  VARIABLES:                                                           *
C                                                                       *
C                                                                       *
C               SM:     3-D vector with s/c position in cartesian       *
C                       SM coordinates.                                 *
C                                                                       *
C                                                                       *
C  ERROR HANDLING:                                                      *
C                                                                       *
C                                                                       *
C  DESIGN AND CODING:   Existing SSC routine adapted for this           *
C                       release by Mauricio Peredo on June 24, 1991.    *
C                                                                       *
C   ADDRESS:            MAURICIO PEREDO                                 *
C                       CODE 695                                        *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       GREENBELT, MARYLAND 20771                       *
C                       USA                                             *
C                       TELEPHONE # (301) 286 - 1526                    *
C                       E-MAIL:  NCF::PEREDO                            *
C                                                                       *
C                                                                       *
C  MODIFICATIONS/UPDATES:                                               *
C                                                                       *
C                                                                       *
C       10/23/92 -- M. Peredo                                           *
C       Criterion for inside v.s. outside plasmasphere corrected        *
C       to be log(n) > 1.5 ==> inside                                   *
C                                                                       *
C       10/27/92  -- M. Peredo                                          *
C   Corrected test for THETA range in subrouten PSPH_V2 to reflect  *
C   the fact that CARSPH_V2 returns radius, latitude, longitude     *
C   rather than colatitude. The test now computes theta and does    *
C   the comparison. For clarity the test was left using THETA       *
C   rather than using colat which would have saved the computation  *
C   this could be ammended at a later date if desired.              *
C                                                                       *
C                                                                       *
C                                                                       *
C********1*********2*********3*********4*********5*********6*********7***
C
C
C
      SUBROUTINE PSPH_V2(SM,IREG)
C
        IMPLICIT NONE
        INCLUDE 'parms.inc'
C
c        real SM(3), SMSPH(3)
c        real LDEN
        DOUBLE PRECISION SM(3),SMSPH(3),LDEN
C
C    ILT is not used, therefore removed  - 9/23/93 (DJH)
C
C        INTEGER IREG,ILT
        INTEGER IREG
C
C       Obtain SM position in spherical coordinates (remember we need
C       angles in radians before calling LOGDEN_V2)
C
        CALL CARSPH_V2(SM,SMSPH)
C
C       CHECK CRITERIA ON R AND THETA TO SEE IF WE MUST
C       EXIT WITHOUT COMPUTING LOG(N)
C
C       IF R < 1.05 MODEL INVALID - EXIT W/O CHANGING REGION
        IF ( SMSPH(1).LE.1.05 ) RETURN
C
C       IF THETA <= 28 OR THETA >= 152 POINT IS OUTSIDE PLASMASPHERE
        IF ( ( (HALFPI-SMSPH(2) ).LE.28.*DEG2RD).OR.
     1       ( (HALFPI-SMSPH(2) ).GE.152.*DEG2RD) ) RETURN
C
C       IF R > 6, POINT IS OUTSIDE - EXIT WITHOUT CHANGING REGION
        IF (SMSPH(1).GT.6.0) RETURN
C
C       GET HERE FOR POINTS THAT COULD BE IN PLASMASPHERE -- PROCEED
C       TO COMPUTE LOG(N) AND CHECK RELATIVE TO SET VALUE LOG(N)=1.5
C       WHICH HAS BEEN CHOSEN TO IDENTIFY THE BOUNDARY.
C
C       Now call LOGDEN_V2 to obtain log(n) at the s/c position
c
        CALL LOGDEN_V2(SMSPH(1),SMSPH(2),SMSPH(3),LDEN)
C
C       IF LOG(N) > 1.5 POINT IS INSIDE -- LABEL IREG ACCORDINGLY
C
        IF (LDEN.LE.1.5) RETURN
C
C       GET HERE IF INSIDE CHANGE IREG TO PLASMASPHERE (DAY/NIGHT)
C       NOTICE WE USE THE CURRENT LABELS OF IREG TO DETERMINE IF
C       POINT IS ON DAY/NIGHT SIDE. THIS ASSURES THAT WE USE THE
C       SAME DEFINITION FOR THE DAY/NIGHT BOUNDARY. NAMELY, THE 
C       PLANE X-GSE = 0.
C
        IF (IREG.EQ.DMSPH) IREG = DPSPH
        IF (IREG.EQ.NMSPH) IREG = NPSPH
C       
      RETURN
      END
C


C************************************************************************
C                                                                       *
C SUBROUTINE:   LOGDEN_V2.FOR                                           *
C               CREATED: MARCH 3, 1992   PROJECT: NSSDC/SSC             *
C                                                                       *
C  ENGLISH NAME: Log(n) = Log(number density)                           *
C  LANGUAGE: FORTRAN77                                                  *
C                                                                       *
C                                                                       *
C  CALLING SEQUENCE:    CALL LOGDEN_V2(R,THETA,PHI,LOGDEN)              *
C                                                                       *
C                                                                       *
C  PURPOSE:     To compute the logarithm of the number density          *
C               according to model of Gallagher, et.al.                 *
C                                                                       *
C  METHOD:      The subroutine receives the spacecraft position in      *
C               spherical SM coordinates (angles in radians), and       *
C               returns log(n) at the s/c position according to model   *
C               of Gallagher, Craven and Comfort [Adv. Space Res.       *
C               Vol. 8, pp 15-24, 1988].                                *
c               The model consists of an empirical formula for the      *
C               plasma density (n) as a function of L=McIlwain's        *
C               L-parameter, MLT=magnetic local time, h(L,lamda)=height *
C               above Earth's surface, NOTE: BY TRIAL AND ERROR, I HAVE *
C               FOUND THAT h SHOULD BE IN KM where lamda=geomagnetic    *
C               latitude.  Free parameters in the model were determined *
C               by fitting to DE 1 RIMS observations.                   *
C                                                                       *
C                                                                       *
C  INPUT/OUTPUT                                                         *
C                                                                       *
C               R = Radial position of s/c                              *
C               THETA = s/c latitude (radians)                          *
C               PHI = s/c longitude (radians)                           *
C                                                                       *
C  OUTPUT                                                               *
C                                                                       *
C       LOGDEN =  log(n) = log(number density)                          *
C                                                                       *
C  CALLS:                                                               *
C               none                                                    *
C                                                                       *
C                                                                       *
C  VARIABLES:                                                           *
C                                                                       *
C                                                                       *
C  ERROR HANDLING:                                                      *
C                                                                       *
C                                                                       *
C  DESIGN AND CODING:   MAURICIO PEREDO                                 *
C                       HUGHES STX CORPORATION                          *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                                                                       *
C   ADDRESS:            MAURICIO PEREDO                                 *
C                       CODE 695                                        *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       GREENBELT, MARYLAND 20771                       *
C                       USA                                             *
C                       TELEPHONE # (301) 286 - 1526                    *
C                       E-MAIL:  NCF::PEREDO                            *
C                                                                       *
C                                                                       *
C  MODIFICATIONS/UPDATES:                                               *
C                                                                       *
C                                                                       *
C********1*********2*********3*********4*********5*********6*********7***
C
        SUBROUTINE LOGDEN_V2(R,THETA,PHI,LDEN)
C
        IMPLICIT NONE
        INCLUDE 'parms.inc'
C
c        real R,THETA,PHI,LDEN,A1,A2,A3,A4,A5,A6,
        DOUBLE PRECISION R,THETA,PHI,LDEN,A1,A2,A3,A4,A5,A6,
     1                   A7,A8,A9,F,G,H,X,MLT,C2LAM
C The following line (REAL*16) was added on 4/16/92 - Douglas J. Hoffman
C       REAL*16 QR,QC2LAM,QA8,QA9,QH
C The preceding was removed on 9/23/93 - DJH, another bug fix
C       below (C2LAM) causes this not to be needed
C
C
C       DEFINE FIXED PARAMETERS
C
        A1 = 1.4
        A2 = 1.53
        A3 = -0.036
        A4 = 30.76
        A5 = 159.9
        A7 = 6.27
C
C       COMPUTE MLT AND X -- NOTE 0 <= MLT < 24 AND -12 <= X <= 12
C
        MLT = (PHI*RAD/15.) - 12.
        X = MLT
        IF (MLT.GE.24.) MLT = MLT - 24.
        IF (MLT.LT.0.) MLT = MLT + 24.
        IF (X.GT.12.) X = X - 24.
        IF (X.LT.-12.) X = X + 24.
C
C       TYPE *,'MLT,X ',MLT,X
C       COMPUTE PARAMETERS DEPENDING ON MLT AND X
C
        A6 = -0.87 + 0.12 * EXP(-X*X/9.)
        A8 = 0.7 * COS( 2*PI*(MLT-21.)/24. ) + 4.4
        A9 = 15.3 * COS( 2*PI*MLT/24. ) + 19.7
c        A6 = -0.87 + 0.12 * DEXP(-X*X/9.)
c        A8 = 0.7 * DCOS( 2*PI*(MLT-21.)/24. ) + 4.4
c        A9 = 15.3 * DCOS( 2*PI*MLT/24. ) + 19.7
C
C       NOW COMPUTE AUXILIARY FUNCTIONS F,G,H
C
        F = A2 - EXP( A3 * (1.-A4 * EXP( 6371.2*(1.-R)/A5 ) ) )
c        F = A2 - DEXP( A3 * (1.-A4 * DEXP( 6371.2*(1.-R)/A5 ) ) )
C
C       The computation of C2LAM was changed to use latitude, not
C       co-latitude.  DJH 9/23/93
C
        C2LAM = COS(THETA)*COS(THETA)
c        C2LAM = DCOS(THETA)*DCOS(THETA)
C        C2LAM = DCOS(HALFPI-THETA)*DCOS(HALFPI-THETA)
        G = (A6*R/C2LAM) + A7
C
C      using real*16 due to potential overflow when computing H (VAX)
C      The range for a real*16 are 0.84Q4932 to 0.59Q4932
C      The range for a real*8  are 0.29D-38  to 1.7D38 (VAX)
C
C      see 'Programming in VAX FORTRAN' v4.0 sec 6.2.1.2.1
C
C      The originial computations of H and LDEN are commented out
C
C      NOTE: Real*16 is a VAX Extension
C
C      Douglas J. Hoffman 4/16/92  (DJH)
C
C      The REAL*16 is no longer needed because the
C      bug above (C2LAM 9/23/93) has been fixed 
C             9/23/93 DJH
C
        H = (1.+(R/(C2LAM*A8))**(2.*(A9-1.)))**(-A9/(A9-1.))
C       QR = R
C       QC2LAM = C2LAM
C       QA8 = A8
C       QA9 = A9
C       QH = ( 1.0+(QR/(QC2LAM*QA8))**(QA9+QA9-2.0) )**(-QA9/(QA9-1.0))
C       
C
C       COMPUTE LOG(N)
C
C       QH = QH * A1 * F * G
C
C       Check for underflow - removed because
C       REAL*16 is no longer used
C
C       IF(QH .LT. 1.0Q-36 .AND. QH .GT. -1.0Q-36) THEN
C           LDEN = 0.0
C       ELSE IF(QH .GT. 1.0Q+36) THEN
C           LDEN = 1.0D+36
C       ELSE IF(QH .LT. -1.0Q+36) THEN
C           LDEN = -1.0D+36
C       ELSE
C           LDEN = QH
C       ENDIF
        LDEN = A1*F*G*H
C
C       END OF MODIFICATION DJH
C
        RETURN
        END




C************************************************************************
C                                                                       *
C SUBROUTINE:   ABER.FOR                                                *
C               CREATED: JUNE 19, 1991                                  *
C PROJECTS: NSSDC/SSC AND ISTP/SPOF                                     *
C                                                                       *
C  ENGLISH NAME: Rotation into solar wind aberrated coordinates (for    *
c                either GSE or GSM)                                     *
C  LANGUAGE: FORTRAN77                                                  *
C                                                                       *
C                                                                       *
C  CALLING SEQUENCE:    CALL ABER(XYZ,AXYZ)                             *
C                                                                       *
C                                                                       *
C  PURPOSE:     To rotate input coordinates (GSE or GSM) into solar     *
c               aberrated coordinates.                                  *
C                                                                       *
C  METHOD:      A rotation about the Z-axis by 4 degrees is applied     *
C                                                                       *
C  INPUT/OUTPUT                                                         *
C                                                                       *
C       XYZ =   3 COMPONENT VECTOR WITH S/C POSITION IN GSE or GSM      *
c               COORDINATES                                             *
C                                                                       *
C  OUTPUT                                                               *
C                                                                       *
C       AXYZ = 3 COMPONENT VECTOR WITH Aberrated COORDINATES            *
C                                                                       *
C  CALLS:                                                               *
C               NONE                                                    *
C                                                                       *
C                                                                       *
C                                                                       *
C  DESIGN AND CODING:   MAURICIO PEREDO                                 *
C                       Hughes STX Corporation                          *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       ISTP/GGS SPOF                                   *
C                       Code 695                                        *
C                                                                       *
C   ADDRESS:            MAURICIO PEREDO                                 *
C                       CODE 695                                        *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       GREENBELT, MARYLAND 20771                       *
C                       USA                                             *
C                       PHONE   (301) 286-1526                          *
c                       FAX     (301) 286-1683                          *
C                       E-MAIL: ISTP::PEREDO                            *
c                               peredo@istp1.gsfc.nasa.gov              *
C                                                                       *
C                                                                       *
C  MODIFICATIONS/UPDATES:                                               *
C                                                                       *
C                                                                       *
C********1*********2*********3*********4*********5*********6*********7***
C
      SUBROUTINE ABER(XYZ,AXYZ)
C
        IMPLICIT NONE
        INCLUDE 'parms.inc'
C
c        real XYZ(3),AXYZ(3)
        DOUBLE PRECISION XYZ(3),AXYZ(3)
C
C       There's confusion about these signs.  Look at params.inc
C       to see that COS4DG = 0.9975640502598243   and    SIN4DG = -0.069756473744125301
C       therefore the rotation matrix is 
C       [cos  -sin]
C       [sin  cos]
C
C       as expected. Sign problem clarified?
C
C       Clockwise axis rotation:
C
        AXYZ(1) = COS4DG*XYZ(1) + SIN4DG*XYZ(2)
        AXYZ(2) = -SIN4DG*XYZ(1) + COS4DG*XYZ(2)
        AXYZ(3) = XYZ(3)
C
        RETURN
        END





C************************************************************************
C                                                                       *
C SUBROUTINE:   BLAYERS.FOR                                             *
C               CREATED: JUNE 19, 1991                                  *
C PROJECTS: NSSDC/SSC AND ISTP/SPOF                                     *
C                                                                       *
C  ENGLISH NAME: Boundary layers (HLBL and LLBL)                        *
C  LANGUAGE: FORTRAN77                                                  *
C                                                                       *
C                                                                       *
C  CALLING SEQUENCE:    CALL BLAYERS(AGSM,DBL)                          *
C                                                                       *
C                                                                       *
C  PURPOSE:     To compute the thickness of the boundary layers,        *
c               High Latitude Boundary Layer (HLBL) or Low Latitude     *
c               Boundary Layer (LLBL) at the aberrated X-GSM of the     *
c               spacecraft. This thicknes is used by the main region    *
c               program SCREG.FOR to determine if the s/c is in         *
c               either of these boundary layers.                        *
C                                                                       *
C  METHOD:      We use the model proposed by R. Parthasarthy for        *
c               the thickness of the layers. Namely, a distance         *
c               DBL (inside the Roelof and Sibeck magnetopause)         *
c               that starts at 0.4 Re at the terminator plane and       *
c               increases parabolically towards the nightside until     *
c               -40 Re; beyond that distance the thickness remains      *
c               constant at the value it has at 40 Re; coefficients     *
c               in the parabolic expression are fixed so that at 40 Re  *
c               the thickness is 4 Re.                                  *
C                                                                       *
C  INPUT/OUTPUT                                                         *
C                                                                       *
C       AGSM =  3 COMPONENT VECTOR WITH S/C POSITION IN ABERRATED GSM   *
c               COORDINATES                                             *
C                                                                       *
C  OUTPUT                                                               *
C                                                                       *
C       DBL = Boundary layer thickness at the same X as the s/c         *
C                                                                       *
C  CALLS:                                                               *
C               NONE                                                    *
C                                                                       *
C                                                                       *
C                                                                       *
C  DESIGN AND CODING:   MAURICIO PEREDO                                 *
C                       Hughes STX Corporation                          *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       ISTP/GGS SPOF                                   *
C                       Code 695                                        *
C                                                                       *
C   ADDRESS:            MAURICIO PEREDO                                 *
C                       CODE 695                                        *
C                       NASA/GODDARD SPACE FLIGHT CENTER                *
C                       GREENBELT, MARYLAND 20771                       *
C                       USA                                             *
C                       PHONE   (301) 286-1526                          *
c                       FAX     (301) 286-1683                          *
C                       E-MAIL: ISTP::PEREDO                            *
c                               peredo@istp1.gsfc.nasa.gov              *
C                                                                       *
C                                                                       *
C  MODIFICATIONS/UPDATES:                                               *
C                                                                       *
C                                                                       *
C********1*********2*********3*********4*********5*********6*********7***
C
C
C
      SUBROUTINE BLAYERS(AGSM,DBL)
C
        IMPLICIT NONE
        INCLUDE 'parms.inc'
C
c        real AGSM(3)
c        real DBL
        DOUBLE PRECISION AGSM(3),DBL
C
        IF (AGSM(1).GT.0.) THEN
           DBL = 0.
        ELSE
           IF (AGSM(1).GE.-40.) THEN
              DBL = 0.4 + 0.0025*AGSM(1)*AGSM(1)
           ELSE
              DBL = 4.0
           ENDIF
        ENDIF
C
        RETURN
        END


