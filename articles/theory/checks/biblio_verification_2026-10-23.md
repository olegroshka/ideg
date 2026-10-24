# Bibliographic verification — 24 items

Date of check: 2026-10-23. Method: WebSearch (standard; extended only for item 2) followed by WebFetch of an authoritative record. Every value in the "on fetched page" column comes from the fetched page/record named under the item; nothing is filled from memory. Where a publisher HTML page could not be fetched (Project Euclid renders client-side and returned empty bodies; Springer loops through its cookie gateway; AMS, MDPI, IEEE, Taylor & Francis, PubMed, UC Press/De Gruyter, Stanford PURL returned 403/405/TLS errors), the publisher-deposited Crossref record for the DOI (`api.crossref.org/works/<DOI>`) and/or the arXiv abstract page's journal-reference line were used. The source class is stated per item.

Verdict key: MATCH = field agrees with the fetched record; MISMATCH = field disagrees; NOT-ON-PAGE = the fetched record does not carry the field; UNVERIFIED = no authoritative record could be fetched.

---

## 1. Stein (1956), Inadmissibility of the usual estimator for the mean of a multivariate normal distribution

Fetched: https://api.crossref.org/works/10.1525/9780520313880-018 (Crossref record deposited by University of California Press). Also attempted: Project Euclid TOC `bsmsp/1200501640` (empty body), Project Euclid chapter page (403), DTIC citation page AD1028390 (403), De Gruyter/UC Press pages (405).

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Stein, C. | Charles Stein | MATCH |
| title | Inadmissibility of the usual estimator for the mean of a multivariate normal distribution | INADMISSIBILITY OF THE USUAL ESTIMATOR FOR THE MEAN OF A MULTIVARIATE NORMAL DISTRIBUTION | MATCH |
| venue | Proc. Third Berkeley Symp. Math. Statist. Prob. | container-title: "Contribution to the Theory of Statistics"; publisher: University of California Press | NOT-ON-PAGE (symposium name not in record; container is the volume subtitle) |
| volume | Vol. 1 | not present in record | NOT-ON-PAGE |
| pages | 197-206 | 197-206 | MATCH |
| year | 1956 | 1956 | MATCH |
| DOI | (none given) | 10.1525/9780520313880-018 (electronic ISBN 9780520313880) | available, not in citation |
| arXiv | (none) | none | n/a |

---

## 2. James & Stein (1961), Estimation with quadratic loss

Fetched: https://api.crossref.org/works?query.bibliographic=James+Stein+Estimation+with+quadratic+loss+Fourth+Berkeley+Symposium+1961&rows=3 — returned only the 1992 reprint: W. James; Charles Stein, "Estimation with Quadratic Loss", Breakthroughs in Statistics (Springer Series in Statistics), pp. 443–460, 1992, DOI 10.1007/978-1-4612-0919-5_30, Springer New York. No record of the 1961 original was fetched. Attempted and failed: Project Euclid landing `euclid.bsmsp/1200512173` (empty), `/ebook/Download?urlId=bsmsp%2F1200512173` (empty), `/download/pdf_1/euclid.bsmsp/1200512173` (403), chapter page and chapter PDF under `/ebooks/...` and `/proceedings/...` (403), Fourth Symposium TOC `bsmsp/1200512153` (403), Crossref date-filtered query (no hit), SWOV library record (bot wall), BibSonomy (bot wall).

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | James, W. & Stein, C. | W. James; Charles Stein (1992 reprint record) | MATCH (reprint only) |
| title | Estimation with quadratic loss | Estimation with Quadratic Loss (1992 reprint record) | MATCH (reprint only) |
| venue | Proc. Fourth Berkeley Symp. Math. Statist. Prob. | not fetched | UNVERIFIED |
| volume | Vol. 1 | not fetched | UNVERIFIED |
| pages | 361-379 | not fetched | UNVERIFIED |
| year | 1961 | not fetched | UNVERIFIED |
| DOI | (none) | none fetched for original | UNVERIFIED |

Overall: UNVERIFIED — no authoritative page for the 1961 original could be fetched; only authors and title are confirmed, via the Springer reprint record.

---

## 3. Brown (1971), Admissible estimators, recurrent diffusions, and insoluble boundary value problems

Fetched: https://api.crossref.org/works/10.1214/aoms/1177693318 (Crossref record deposited by the Institute of Mathematical Statistics). Project Euclid landing page `euclid.aoms/1177693318` returned an empty body; UPenn repository page returned 403.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Brown, L. D. | L. D. Brown | MATCH |
| title | Admissible estimators, recurrent diffusions, and insoluble boundary value problems | Admissible Estimators, Recurrent Diffusions, and Insoluble Boundary Value Problems | MATCH |
| venue | Ann. Math. Statist. | The Annals of Mathematical Statistics | MATCH |
| volume(issue) | 42(3) | 42, issue 3 | MATCH |
| pages | 855-903 | 855-903 | MATCH |
| year | 1971 | 1971 | MATCH |
| DOI | (none given) | 10.1214/aoms/1177693318 | available, not in citation |

---

## 4. Komaki (2006), Shrinkage priors for Bayesian prediction

Fetched: https://api.crossref.org/works/10.1214/009053606000000010 (IMS-deposited Crossref record). Project Euclid `.full` and `.pdf` pages returned empty bodies.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Komaki, F. | Fumiyasu Komaki | MATCH |
| title | Shrinkage priors for Bayesian prediction | Shrinkage priors for Bayesian prediction | MATCH |
| venue | Ann. Statist. | The Annals of Statistics | MATCH |
| volume(issue) | 34(2) | 34, issue 2 | MATCH |
| pages | 808-819 | 808-819 | MATCH |
| year | 2006 | 2006 | MATCH |
| DOI | (none given) | 10.1214/009053606000000010 | available, not in citation |
| arXiv | (none given) | not on fetched record (search results listed math/0607021; not fetched) | NOT-ON-PAGE |

---

## 5. Amari & Nagaoka (2000), Methods of Information Geometry

Fetched: (a) https://ci.nii.ac.jp/ncid/BD14356090 (CiNii / National Institute of Informatics catalog record); (b) https://api.crossref.org/works/10.1090/mmono/191 (Crossref record deposited by the American Mathematical Society). AMS bookstore, ams.org/books/mmono/191 and the AMS endmatter PDF all returned 403; OUP product page returned empty; WorldCat ISBN search returned no results page.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Amari, S. & Nagaoka, H. | (a) "Shun-ichi Amari, Hiroshi Nagaoka ; translated by Daishi Harada"; (b) Shun-ichi Amari; Hiroshi Nagaoka | MATCH |
| title | Methods of Information Geometry | (a) Methods of information geometry; (b) Methods of Information Geometry | MATCH |
| publisher | AMS / Oxford University Press | (a) American Mathematical Society, Oxford University Press; place "Providence, Rhode Island, [Oxford]"; (b) American Mathematical Society only | MATCH (OUP co-publisher appears on the NII catalog record; Crossref lists AMS only) |
| series | Translations of Mathematical Monographs vol. 191 | (a) "Translations of mathematical monographs, volume 191"; (b) Translations of Mathematical Monographs, DOI suffix mmono/191 | MATCH |
| year | 2000 | (a) "[2000], c2000"; (b) published-print 2007-04-13 | MATCH on (a); (b) carries the 2007 print date (ISBN 9780821843024 edition) |
| DOI | (none given) | 10.1090/mmono/191 | available, not in citation |
| ISBN | (none given) | (a) 9780821843024; (b) 9780821843024, 9781470446055 | available, not in citation |
| other | — | (a) x, 206 pages; "Originally published in Japanese: Tokyo : Iwanami Shoten, 1993" | — |

Note: no publisher HTML page could be fetched; verification rests on the AMS-deposited Crossref record plus the NII catalog record.

---

## 6. Perelman (2002), The entropy formula for the Ricci flow and its geometric applications

Fetched: https://arxiv.org/abs/math/0211159

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Perelman, G. | Grisha Perelman | MATCH |
| title | The entropy formula for the Ricci flow and its geometric applications | The entropy formula for the Ricci flow and its geometric applications | MATCH |
| venue | arXiv | arXiv (math.DG; MSC 53C); "Submitted on 11 Nov 2002"; no journal reference listed | MATCH |
| arXiv id | math/0211159 | math/0211159 | MATCH |
| year | 2002 | 2002 (v1 Mon, 11 Nov 2002) | MATCH |
| DOI | (none) | arXiv-issued 10.48550/arXiv.math/0211159 only | n/a |

---

## 7. Jacobson (1995), Thermodynamics of Spacetime: The Einstein Equation of State

Fetched: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.75.1260 (APS publisher page); https://arxiv.org/abs/gr-qc/9504004; https://api.crossref.org/works/10.1103/PhysRevLett.75.1260

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Jacobson, T. | Ted Jacobson | MATCH |
| title | Thermodynamics of Spacetime: The Einstein Equation of State | Thermodynamics of Spacetime: The Einstein Equation of State | MATCH |
| venue | Phys. Rev. Lett. | Phys. Rev. Lett. | MATCH |
| volume(issue) | 75(7) | Vol. 75, Iss. 7 (14 August 1995) | MATCH |
| pages | 1260-1263 | APS page shows start page 1260 only; Crossref 1260-1263; arXiv journal-ref "Phys.Rev.Lett.75:1260-1263,1995" | MATCH |
| year | 1995 | 1995 | MATCH |
| DOI | (none given) | 10.1103/PhysRevLett.75.1260 | available, not in citation |
| arXiv | (none given) | gr-qc/9504004 (v2 6 Jun 1995) | available, not in citation |

---

## 8. Connes & Rovelli (1994), Von Neumann algebra automorphisms and time-thermodynamics relation in generally covariant quantum theories

Fetched: https://iopscience.iop.org/article/10.1088/0264-9381/11/12/007 (IOP publisher page). Citation line on page: "A Connes and C Rovelli 1994 Class. Quantum Grav. 11 2899".

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Connes, A. & Rovelli, C. | A Connes and C Rovelli | MATCH |
| title | Von Neumann algebra automorphisms and time-thermodynamics relation in generally covariant quantum theories | Von Neumann algebra automorphisms and time-thermodynamics relation in generally covariant quantum theories | MATCH |
| venue | Class. Quantum Grav. | Classical and Quantum Gravity | MATCH |
| volume(issue) | 11(12) | Volume 11, Number 12 | MATCH |
| pages | 2899 | 2899 | MATCH |
| year | 1994 | 1994 (received 23 May 1994) | MATCH |
| DOI | (none given) | 10.1088/0264-9381/11/12/007 | available, not in citation |
| arXiv | (none given) | not on IOP page (search results listed gr-qc/9406019; not fetched) | NOT-ON-PAGE |

---

## 9. Chirco, Haggard, Riello & Rovelli (2014), Spacetime thermodynamics without hidden degrees of freedom

Fetched: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.90.044044 (APS publisher page); https://arxiv.org/abs/1401.5262

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Chirco, G., Haggard, H. M., Riello, A. & Rovelli, C. | Goffredo Chirco, Hal M. Haggard, Aldo Riello, and Carlo Rovelli | MATCH |
| title | Spacetime thermodynamics without hidden degrees of freedom | Spacetime thermodynamics without hidden degrees of freedom | MATCH |
| venue | Phys. Rev. D | Phys. Rev. D | MATCH |
| volume(issue) | 90(4) | Vol. 90, Iss. 4 (15 August 2014) | MATCH |
| article no. | 044044 | 044044 | MATCH |
| year | 2014 | Published 15 August 2014 | MATCH |
| DOI | (none given) | 10.1103/PhysRevD.90.044044 | available, not in citation |
| arXiv | (none given) | arXiv:1401.5262 [gr-qc], submitted 21 Jan 2014; journal-ref "Phys. Rev. D 90, 044044 (2014)" | available, not in citation |

---

## 10. Stein (1981), Estimation of the mean of a multivariate normal distribution

Fetched: https://api.crossref.org/works/10.1214/aos/1176345632 (IMS-deposited Crossref record). Project Euclid landing and Download endpoints returned empty bodies.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Stein, C. | Charles M. Stein | MATCH |
| title | Estimation of the mean of a multivariate normal distribution | Estimation of the Mean of a Multivariate Normal Distribution | MATCH |
| venue | Ann. Statist. | The Annals of Statistics | MATCH |
| volume(issue) | 9(6) | 9, issue 6 | MATCH |
| pages | 1135-1151 | 1135-1151 | MATCH |
| year | 1981 | 1981 | MATCH |
| DOI | (none given) | 10.1214/aos/1176345632 | available, not in citation |

---

## 11. George, Liang & Xu (2006), Improved minimax predictive densities under Kullback-Leibler loss

Fetched: https://api.crossref.org/works/10.1214/009053606000000155 (IMS-deposited Crossref record). Project Euclid `.full` and `.pdf` pages returned empty bodies.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | George, E. I., Liang, F. & Xu, X. | Edward I. George; Feng Liang; Xinyi Xu | MATCH |
| title | Improved minimax predictive densities under Kullback-Leibler loss | Improved minimax predictive densities under Kullback–Leibler loss (en dash) | MATCH (dash style only) |
| venue | Ann. Statist. | The Annals of Statistics | MATCH |
| volume(issue) | 34(1) | 34, issue 1 | MATCH |
| pages | 78-91 | 78-91 | MATCH |
| year | 2006 | 2006 | MATCH |
| DOI | (none given) | 10.1214/009053606000000155 | available, not in citation |
| arXiv | (none given) | not on record (search results listed math/0605432; not fetched) | NOT-ON-PAGE |

---

## 12. Baranchik (1964), Multiple regression and estimation of the mean of a multivariate normal distribution

Fetched: https://statistics.stanford.edu/technical-reports/multiple-regression-and-estimation-mean-multivariate-normal-distribution (Stanford Department of Statistics technical-report listing). PURL (`purl.stanford.edu/hq883mw7116`, `.mods`, `.json`) failed on TLS certificate; SearchWorks returned empty.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Baranchik, A. J. | A.J. Baranchik | MATCH |
| title | Multiple regression and estimation of the mean of a multivariate normal distribution | Multiple Regression and Estimation of the Mean of a Multivariate Normal Distribution | MATCH |
| venue | Technical Report, Department of Statistics, Stanford University | Department of Statistics, Stanford University; Report Number "CHE ONR 51"; Stanford Digital Repository link purl.stanford.edu/hq883mw7116 | MATCH |
| report no. | No. 51 | "CHE ONR 51" | MATCH (number 51; page shows the ONR-series label) |
| year | 1964 | Report Date "May 1964" | MATCH |
| DOI | (none) | none | n/a |

---

## 13. Efron & Morris (1973), Stein's estimation rule and its competitors - an empirical Bayes approach

Fetched: https://api.crossref.org/works/10.1080/01621459.1973.10481350 (Crossref record deposited by Informa UK / Taylor & Francis). The T&F abstract page itself returned 403; the T&F search-result title read "Journal of the American Statistical Association: Vol 68, No 341".

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Efron, B. & Morris, C. | Bradley Efron; Carl Morris | MATCH |
| title | Stein's estimation rule and its competitors - an empirical Bayes approach | Stein's Estimation Rule and its Competitors—An Empirical Bayes Approach (em dash) | MATCH (dash style only) |
| venue | J. Amer. Statist. Assoc. | Journal of the American Statistical Association | MATCH |
| volume(issue) | 68(341) | 68, issue 341 | MATCH |
| pages | 117-130 | 117-130 | MATCH |
| year | 1973 | 1973 | MATCH |
| DOI | (none given) | 10.1080/01621459.1973.10481350 | available, not in citation |

---

## 14. Efron (2011), Tweedie's formula and selection bias

Fetched: https://api.crossref.org/works/10.1198/jasa.2011.tm11181 (Informa-deposited Crossref record); https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:22505788&format=json&resultType=lite (Europe PMC record). T&F page and PubMed/Europe PMC HTML returned 403 or a cookie wall.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Efron, B. | Bradley Efron / "Efron B." | MATCH |
| title | Tweedie's formula and selection bias | Tweedie's Formula and Selection Bias | MATCH |
| venue | J. Amer. Statist. Assoc. | Journal of the American Statistical Association / J Am Stat Assoc | MATCH |
| volume(issue) | 106(496) | 106, issue 496 | MATCH |
| pages | 1602-1614 | 1602-1614 | MATCH |
| year | 2011 | 2011 | MATCH |
| DOI | (none given) | 10.1198/jasa.2011.tm11181; PMID 22505788 | available, not in citation |

---

## 15. Komaki (1996), On asymptotic properties of predictive distributions

Fetched: https://api.crossref.org/works?query.bibliographic=Komaki+On+asymptotic+properties+of+predictive+distributions+Biometrika+1996&rows=3 (first hit; Crossref record deposited by Oxford University Press). OUP article page not fetched.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Komaki, F. | F Komaki | MATCH |
| title | On asymptotic properties of predictive distributions | On asymptotic properties of predictive distributions | MATCH |
| venue | Biometrika | Biometrika (Oxford University Press) | MATCH |
| volume(issue) | 83(2) | 83, issue 2 | MATCH |
| pages | 299-313 | 299-313 | MATCH |
| year | 1996 | 1996 | MATCH |
| DOI | (none given) | 10.1093/biomet/83.2.299 | available, not in citation |

---

## 16. Liang & Barron (2004), Exact minimax strategies for predictive density estimation, data compression, and model selection

Fetched: https://api.crossref.org/works?query.bibliographic=Liang+Barron+Exact+minimax+strategies+for+predictive+density+estimation+data+compression+and+model+selection&rows=3 (second hit; Crossref record deposited by IEEE). IEEE Xplore document page 1347357 returned an empty body. Note: the same query also returned a distinct 2002 ISIT abstract (DOI 10.1109/isit.2002.1023421, p. 149) and a 2005 MIT Press chapter — neither is the cited item.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Liang, F. & Barron, A. | F. Liang; A. Barron | MATCH |
| title | Exact minimax strategies for predictive density estimation, data compression, and model selection | Exact Minimax Strategies for Predictive Density Estimation, Data Compression, and Model Selection | MATCH |
| venue | IEEE Trans. Inform. Theory | IEEE Transactions on Information Theory | MATCH |
| volume(issue) | 50(11) | 50, issue 11 | MATCH |
| pages | 2708-2726 | 2708-2726 | MATCH |
| year | 2004 | 2004 | MATCH |
| DOI | (none given) | 10.1109/tit.2004.836922 | available, not in citation |

---

## 17. Buchert (2000), On average properties of inhomogeneous fluids in general relativity: dust cosmologies

Fetched: https://api.crossref.org/works/10.1023/A:1001800617177 (Springer-deposited Crossref record). Springer article page redirected to the idp.springer.com cookie gateway in a loop and could not be read.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Buchert, T. | Thomas Buchert | MATCH |
| title | On average properties of inhomogeneous fluids in general relativity: dust cosmologies | On Average Properties of Inhomogeneous Fluids in General Relativity: Dust Cosmologies | MATCH |
| venue | Gen. Relativ. Gravit. | General Relativity and Gravitation | MATCH |
| volume(issue) | 32 | 32, issue 1 | MATCH (issue not given in citation) |
| pages | 105-125 | 105-125 | MATCH |
| year | 2000 | 2000 | MATCH |
| DOI | (none given) | 10.1023/A:1001800617177 | available, not in citation |
| arXiv | (none given) | not on record (search results listed gr-qc/9906015; not fetched) | NOT-ON-PAGE |

---

## 18. Bakry & Emery (1985), Diffusions hypercontractives

Fetched: (a) https://www.numdam.org/item/SPS_1985__19__177_0 (Numdam, the French mathematics digital library hosting the Séminaire); (b) https://api.crossref.org/works/10.1007/BFb0075847 (Springer-deposited chapter record); (c) https://api.crossref.org/works?filter=isbn:9783540152309,type:book&rows=2 (Springer-deposited book record, DOI 10.1007/bfb0075834); (d) https://ftp.math.utah.edu/pub/tex/bib/idx/lnm1985/1123/0/177-206.html (third-party BibTeX bibliography). Springer chapter HTML looped on the cookie gateway.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Bakry, D. & Emery, M. | (a) Dominique Bakry; Michel Émery; (b) D. Bakry; M. Émery | MATCH with orthographic correction: Émery (accent) |
| title | Diffusions hypercontractives | Diffusions hypercontractives | MATCH |
| venue | Seminaire de probabilites XIX | (a) Séminaire de probabilités, Tome 19 (1985); (b)/(c) "Séminaire de Probabilités XIX 1983/84", eds Jacques Azéma, Marc Yor, Springer Berlin Heidelberg | MATCH (accents: Séminaire de probabilités) |
| series/volume | Lecture Notes in Math. 1123 | (b)/(c) Lecture Notes in Mathematics (ISSN 0075-8434), volume number not present; ISBN 9783540152309 / 3-540-15230-X; (d) volume "1123" with the same ISBN | MATCH (LNM 1123 appears only on the third-party bibliography (d); publisher-deposited records carry the series and ISBN but no volume number) |
| pages | 177-206 | 177-206 | MATCH |
| year | 1985 | 1985 | MATCH |
| DOI | (none given) | 10.1007/BFb0075847; MR 889476; Zbl 0561.60080 | available, not in citation |

---

## 19. Hartigan (1998), The maximum likelihood prior

Fetched: https://api.crossref.org/works/10.1214/aos/1024691462 (IMS-deposited Crossref record). Project Euclid `.full` and `.pdf` pages returned empty bodies.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Hartigan, J. A. | J. A. Hartigan | MATCH |
| title | The maximum likelihood prior | The maximum likelihood prior | MATCH |
| venue | Ann. Statist. | The Annals of Statistics | MATCH |
| volume(issue) | 26(6) | 26, issue 6 | MATCH |
| pages | 2083-2103 | 2083-2103 | MATCH |
| year | 1998 | 1998 | MATCH |
| DOI | (none given) | 10.1214/aos/1024691462 | available, not in citation |

---

## 20. Padmanabhan (2010), Thermodynamical aspects of gravity: new insights

Fetched: https://iopscience.iop.org/article/10.1088/0034-4885/73/4/046901 (IOP publisher page). Citation line on page: "T Padmanabhan 2010 Rep. Prog. Phys. 73 046901".

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Padmanabhan, T. | T Padmanabhan (IUCAA, Pune) | MATCH |
| title | Thermodynamical aspects of gravity: new insights | Thermodynamical aspects of gravity: new insights | MATCH |
| venue | Rep. Prog. Phys. | Reports on Progress in Physics | MATCH |
| volume(issue) | 73 | Volume 73, Number 4 | MATCH (issue not given in citation) |
| article no. | 046901 | 046901 | MATCH |
| year | 2010 | 2010 (received 25 Nov 2009; published 25 Mar 2010) | MATCH |
| DOI | (none given) | 10.1088/0034-4885/73/4/046901 | available, not in citation |
| arXiv | (none given) | not on IOP page (search results listed 0911.5004; not fetched) | NOT-ON-PAGE |

---

## 21. Verlinde (2011), On the origin of gravity and the laws of Newton

Fetched: https://api.crossref.org/works/10.1007/JHEP04(2011)029 (Springer-deposited Crossref record); https://arxiv.org/abs/1001.0785. Springer article HTML looped on the cookie gateway.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Verlinde, E. | Crossref: Erik Verlinde; arXiv: Erik P. Verlinde | MATCH |
| title | On the origin of gravity and the laws of Newton | Crossref: On the origin of gravity and the laws of Newton; arXiv: On the Origin of Gravity and the Laws of Newton | MATCH |
| venue | JHEP | Journal of High Energy Physics | MATCH |
| volume(issue) | 2011(4) | volume 2011, issue 4 | MATCH |
| article no. | 29 | article number 29; arXiv journal-ref "JHEP 1104:029,2011" | MATCH |
| year | 2011 | 2011 | MATCH |
| DOI | (none given) | 10.1007/JHEP04(2011)029 | available, not in citation |
| arXiv | (none given) | arXiv:1001.0785 [hep-th], submitted 6 Jan 2010 | available, not in citation |

---

## 22. Hu & Verdaguer (2008), Stochastic gravity: theory and applications

Fetched: https://api.crossref.org/works/10.12942/lrr-2008-3 (Springer-deposited Crossref record); https://arxiv.org/abs/0802.0658. Springer article HTML looped on the cookie gateway.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Hu, B. L. & Verdaguer, E. | Crossref: Bei Lok Hu; Enric Verdaguer; arXiv: B.L. Hu, E. Verdaguer | MATCH |
| title | Stochastic gravity: theory and applications | Stochastic Gravity: Theory and Applications | MATCH |
| venue | Living Rev. Relativ. | Living Rev. Relativ. | MATCH |
| volume | 11 | Crossref: volume 11, issue 1; arXiv journal-ref "Living Rev. Relativity, 11 (2008) 3" | MATCH |
| article no. | 3 | not present on Crossref record; "3" on arXiv journal-ref line and in DOI suffix lrr-2008-3 | MATCH (via arXiv journal-ref) |
| year | 2008 | 2008 (online 29 May 2008) | MATCH |
| DOI | (none given) | 10.12942/lrr-2008-3 | available, not in citation |
| arXiv | (none given) | arXiv:0802.0658 [gr-qc]; comments: "an update of the 2003 review ... gr-qc/0307032" | available, not in citation |

---

## 23. Caticha (2015), Entropic dynamics

Fetched: https://api.crossref.org/works?query.bibliographic=Caticha+Entropic+Dynamics+Entropy+2015+17+6110&rows=3 (first hit; Crossref record deposited by MDPI AG); https://arxiv.org/abs/1509.03222. MDPI article page returned 403.

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Caticha, A. | Ariel Caticha | MATCH |
| title | Entropic dynamics | Entropic Dynamics | MATCH |
| venue | Entropy | Entropy (MDPI AG) | MATCH |
| volume(issue) | 17(9) | 17, issue 9 | MATCH |
| pages | 6110-6128 | 6110–6128; arXiv journal-ref "Entropy 17, 6110-6128 (2015)" | MATCH |
| year | 2015 | 2015 | MATCH |
| DOI | (none given) | 10.3390/e17096110 | available, not in citation |
| arXiv | (none given) | arXiv:1509.03222 [quant-ph], submitted 10 Sep 2015 | available, not in citation |

---

## 24. Ruppeiner (1995), Riemannian geometry in thermodynamic fluctuation theory

Fetched: https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.67.605 (APS publisher page); https://api.crossref.org/works/10.1103/RevModPhys.67.605

| field | as given | on fetched page | verdict |
|---|---|---|---|
| authors | Ruppeiner, G. | George Ruppeiner | MATCH |
| title | Riemannian geometry in thermodynamic fluctuation theory | Riemannian geometry in thermodynamic fluctuation theory | MATCH |
| venue | Rev. Mod. Phys. | Rev. Mod. Phys. | MATCH |
| volume(issue) | 67 | Vol. 67, Iss. 3 (July–September 1995) | MATCH (issue not given in citation) |
| pages | 605-659 | APS page: 605– (end page not shown); Crossref: 605-659 | MATCH |
| year | 1995 | 1 July 1995 | MATCH |
| DOI | (none given) | 10.1103/RevModPhys.67.605 | available, not in citation |
| erratum | (none given) | "Erratum: Riemannian geometry in thermodynamic fluctuation theory," Rev. Mod. Phys. 68, 313 (1996) | available, not in citation |

---

## Summary

| item | overall verdict | note |
|---|---|---|
| 1. Stein 1956 | VERIFIED | Author, title, pp. 197-206, 1956, UC Press confirmed on UC Press-deposited Crossref record (DOI 10.1525/9780520313880-018); symposium name / "Vol. 1" not on the fetched record. |
| 2. James & Stein 1961 | UNVERIFIED | No authoritative page for the 1961 original fetchable (Project Euclid empty/403; SWOV, BibSonomy bot walls). Authors/title confirmed only via Springer 1992 reprint record. |
| 3. Brown 1971 | VERIFIED | All fields match IMS Crossref record; DOI 10.1214/aoms/1177693318. |
| 4. Komaki 2006 | VERIFIED | All fields match IMS Crossref record; DOI 10.1214/009053606000000010. |
| 5. Amari & Nagaoka 2000 | VERIFIED | Matches NII catalog (AMS + OUP, vol. 191, c2000, tr. Harada) and AMS Crossref record (DOI 10.1090/mmono/191, print date 2007); no AMS/OUP HTML page fetchable. |
| 6. Perelman 2002 | VERIFIED | arXiv abstract page; math/0211159, submitted 11 Nov 2002. |
| 7. Jacobson 1995 | VERIFIED | APS page + Crossref + arXiv; 75(7) 1260-1263; DOI 10.1103/PhysRevLett.75.1260; arXiv gr-qc/9504004. |
| 8. Connes & Rovelli 1994 | VERIFIED | IOP page; "11 2899", Number 12; DOI 10.1088/0264-9381/11/12/007. |
| 9. Chirco et al. 2014 | VERIFIED | APS page + arXiv 1401.5262; 90(4) 044044; DOI 10.1103/PhysRevD.90.044044. |
| 10. Stein 1981 | VERIFIED | IMS Crossref record; author on record is "Charles M. Stein"; DOI 10.1214/aos/1176345632. |
| 11. George, Liang & Xu 2006 | VERIFIED | IMS Crossref record; title uses en dash "Kullback–Leibler"; DOI 10.1214/009053606000000155. |
| 12. Baranchik 1964 | VERIFIED | Stanford Statistics technical-report page; Report Number "CHE ONR 51", May 1964; PURL hq883mw7116. |
| 13. Efron & Morris 1973 | VERIFIED | Informa Crossref record; 68(341) 117-130; title uses em dash; DOI 10.1080/01621459.1973.10481350. |
| 14. Efron 2011 | VERIFIED | Informa Crossref + Europe PMC; 106(496) 1602-1614; DOI 10.1198/jasa.2011.tm11181; PMID 22505788. |
| 15. Komaki 1996 | VERIFIED | OUP Crossref record; 83(2) 299-313; DOI 10.1093/biomet/83.2.299. |
| 16. Liang & Barron 2004 | VERIFIED | IEEE Crossref record; 50(11) 2708-2726; DOI 10.1109/tit.2004.836922 (distinct 2002 ISIT abstract exists; not the cited item). |
| 17. Buchert 2000 | VERIFIED | Springer Crossref record; 32(1) 105-125; DOI 10.1023/A:1001800617177; Springer HTML unreachable. |
| 18. Bakry & Emery 1985 | VERIFIED-WITH-CORRECTIONS | Orthography: "Émery", "Séminaire de probabilités"; pp. 177-206, 1985, eds Azéma & Yor confirmed (Numdam + Springer Crossref); "LNM 1123" confirmed only on a third-party bibliography (same ISBN 3-540-15230-X); DOI 10.1007/BFb0075847. |
| 19. Hartigan 1998 | VERIFIED | IMS Crossref record; 26(6) 2083-2103; DOI 10.1214/aos/1024691462. |
| 20. Padmanabhan 2010 | VERIFIED | IOP page; 73(4) 046901; DOI 10.1088/0034-4885/73/4/046901. |
| 21. Verlinde 2011 | VERIFIED | Springer Crossref + arXiv 1001.0785; 2011(4) art. 29; DOI 10.1007/JHEP04(2011)029; Springer HTML unreachable. |
| 22. Hu & Verdaguer 2008 | VERIFIED | Springer Crossref (vol. 11, issue 1, 2008) + arXiv 0802.0658 journal-ref "11 (2008) 3"; DOI 10.12942/lrr-2008-3. |
| 23. Caticha 2015 | VERIFIED | MDPI Crossref + arXiv 1509.03222; 17(9) 6110-6128; DOI 10.3390/e17096110; MDPI HTML 403. |
| 24. Ruppeiner 1995 | VERIFIED | APS page + Crossref; 67(3) 605-659; DOI 10.1103/RevModPhys.67.605; erratum RMP 68, 313 (1996). |
