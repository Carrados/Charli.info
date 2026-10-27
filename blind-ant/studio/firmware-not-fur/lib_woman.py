def woman(a, eyes_closed=False, outfit="jacket", hair=True):
    # ---------- woman (CJ, 37)
    # back hair: long soft layered waves just below the shoulders
    if hair: a('<path d="M352,560 C300,600 280,660 296,720 C312,770 272,800 288,850 C302,895 262,915 280,955 C292,985 325,990 342,1012 C362,992 382,1002 400,987 L500,987 C518,1002 538,992 558,1012 C575,990 608,985 620,955 C638,915 598,895 612,850 C628,800 588,770 604,720 C620,660 600,600 540,560 Z" fill="url(#hair)"/>')
    # neck
    a('<path d="M405,770 L403,868 C425,885 467,885 489,868 L487,770 Z" fill="#e6b9a1"/>')
    a('<path d="M405,790 C430,822 462,822 487,790 L487,772 C462,800 430,800 405,772Z" fill="#c99780" opacity="0.55"/>')
    if outfit=="jacket":
        a('<path d="M170,1536 L182,1060 C188,990 230,950 300,925 L403,872 L446,1000 L489,872 L592,925 C662,950 704,990 710,1060 L722,1536 Z" fill="url(#coat)"/>')
        a('<path d="M403,872 L446,1040 L489,872 C468,888 424,888 403,872Z" fill="#efe8de"/>')
        a('<path d="M408,872 L446,985 L484,872 C466,884 426,884 408,872Z" fill="#e6b9a1"/>')
        a('<path d="M420,880 C432,930 440,955 446,985 C452,955 460,930 472,880" fill="none" stroke="#d2a28a" stroke-width="2" opacity="0.6"/>')
        a('<path d="M214,1010 C230,980 262,960 296,948 M650,980 C672,1000 690,1030 698,1070 M230,1100 L240,1400 M682,1120 L690,1420" fill="none" stroke="#5c6680" stroke-width="5" stroke-linecap="round" opacity="0.55"/>')
        a('<path d="M300,925 L403,872 L446,1060 L405,1190 L362,1010 L292,975Z" fill="#232838" stroke="#7d8db0" stroke-width="3"/>')
        a('<path d="M592,925 L489,872 L446,1060 L487,1190 L530,1010 L600,975Z" fill="#232838" stroke="#7d8db0" stroke-width="3"/>')
    elif outfit=="coat":
        a('<path d="M150,1536 L168,1060 C176,985 225,945 300,922 L403,876 C430,900 462,900 489,876 L592,922 C665,945 712,985 722,1060 L740,1536 Z" fill="#1b2740"/>')
        a('<path d="M300,922 L403,876 L420,960 L380,1160 L340,1000 Z" fill="#22314f" stroke="#33466e" stroke-width="3"/>')
        a('<path d="M592,922 L489,876 L472,960 L512,1160 L552,1000 Z" fill="#22314f" stroke="#33466e" stroke-width="3"/>')
        a('<path d="M405,960 L446,1536 L487,960 Z" fill="#d9c7a3"/>')
        a('<path d="M360,880 C380,850 420,858 446,866 C472,858 512,850 532,880 C548,910 540,950 520,968 C495,990 400,990 372,968 C352,950 346,910 360,880Z" fill="#e3d5b5"/>')
        a('<path d="M380,905 C410,925 482,925 512,905 M375,940 C410,960 482,960 517,940" fill="none" stroke="#c9b791" stroke-width="5" stroke-linecap="round"/>')
    # face (oval)
    a('<path d="M446,528 C512,528 548,585 546,660 C544,730 505,800 446,808 C387,800 348,730 346,660 C344,585 380,528 446,528Z" fill="url(#skin)"/>')
    a('<path d="M352,690 C362,765 400,798 446,804 C492,798 530,765 540,690 C528,752 492,786 446,790 C400,786 364,752 352,690Z" fill="#d9a990" opacity="0.5"/>')
    # brows
    a('<path d="M382,610 C400,597 424,595 438,603" fill="none" stroke="#4a1418" stroke-width="6" stroke-linecap="round"/>')
    a('<path d="M454,603 C468,595 492,597 510,610" fill="none" stroke="#4a1418" stroke-width="6" stroke-linecap="round"/>')
    if not eyes_closed:
        for cx in (410,482):
            a(f'<path d="M{cx-27},640 Q{cx},622 {cx+27},640 Q{cx},655 {cx-27},640Z" fill="#fbf7f2"/>')
            a(f'<circle cx="{cx+1}" cy="640" r="11" fill="#3d7fb8"/><circle cx="{cx+1}" cy="640" r="5.5" fill="#101820"/><circle cx="{cx+4}" cy="636" r="2.6" fill="#fff"/>')
            a(f'<path d="M{cx-29},641 Q{cx},618 {cx+30},638" fill="none" stroke="#1a1012" stroke-width="4.5" stroke-linecap="round"/>')
            a(f'<path d="M{cx-20},651 Q{cx},658 {cx+20},650" fill="none" stroke="#b98a78" stroke-width="2"/>')
    else:
        for cx in (410,482):
            a(f'<path d="M{cx-26},642 Q{cx},654 {cx+26},641" fill="none" stroke="#1a1012" stroke-width="4.5" stroke-linecap="round"/>')
            a(f'<path d="M{cx-20},645 l-6,7 M{cx-8},651 l-3,8 M{cx+6},651 l2,8 M{cx+18},646 l6,7" stroke="#1a1012" stroke-width="2.5" stroke-linecap="round"/>')
    a('<path d="M447,648 C443,676 436,694 434,703 C442,711 454,711 462,704" fill="none" stroke="#c48d76" stroke-width="3.5" stroke-linecap="round"/>')
    a('<path d="M412,742 C427,732 440,734 447,738 C455,734 468,732 482,742 C470,746 458,748 447,748 C436,748 424,746 412,742Z" fill="#8e1b24"/>')
    a('<path d="M412,742 C426,760 468,760 482,742 C468,748 426,748 412,742Z" fill="#a8232f"/>')
    a('<ellipse cx="394" cy="694" rx="22" ry="12" fill="#e89a8e" opacity="0.28"/><ellipse cx="500" cy="694" rx="22" ry="12" fill="#e89a8e" opacity="0.28"/>')
    # crown and side-swept front, framing the face without covering it
    if hair: a('<path d="M342,650 C330,560 375,500 450,496 C530,494 566,560 552,650 C546,605 525,572 492,560 C470,582 432,590 392,575 C368,592 352,615 346,660 Z" fill="url(#hair)"/>')
    if hair: a('<path d="M344,630 C318,690 338,740 316,800 C298,850 330,890 312,930 C318,950 335,960 352,966 C338,920 360,885 350,840 C340,790 362,740 348,690 C344,670 346,650 350,640Z" fill="url(#hair)"/>')
    if hair: a('<path d="M550,630 C576,690 556,740 578,800 C596,850 564,890 582,930 C576,950 559,960 542,966 C556,920 534,885 544,840 C554,790 532,740 546,690 C550,670 548,650 544,640Z" fill="url(#hair)"/>')
    if hair:
        for d in ['M392,540 C430,520 480,522 520,548','M352,620 C344,690 340,760 328,830','M542,620 C550,690 554,760 566,830','M310,880 C306,920 318,950 340,975','M584,880 C588,920 576,950 554,975','M300,760 C296,800 300,840 292,880','M594,760 C598,800 594,840 602,880']:
            a(f'<path d="{d}" fill="none" stroke="url(#hairhi)" stroke-width="7" stroke-linecap="round"/>')

def dog(a, tilt=0):
    # ---------- robot dog (deliberately not a real guide device)
    a('<g>')
    # body rising from bottom right
    a('<path d="M700,1900 L705,1100 C710,1020 745,975 800,968 C860,962 912,1000 930,1070 L960,1536Z" fill="url(#chrome2)" stroke="#0e1628" stroke-width="4"/>')
    a('<circle cx="840" cy="1120" r="48" fill="none" stroke="#55c8ff" stroke-width="5" opacity="0.85"/><circle cx="840" cy="1120" r="24" fill="#1a2944" stroke="#9fb4cf" stroke-width="4"/>')
    a('<path d="M725,1060 L830,1040 M715,1180 L790,1195 M880,1220 L935,1260" stroke="#9fb4cf" stroke-width="3" opacity="0.7"/>')
    # neck
    a('<path d="M720,980 L745,820 L835,820 L850,975 Z" fill="url(#chrome)" stroke="#0e1628" stroke-width="4"/>')
    for y in (850,880,910,940): a(f'<line x1="742" y1="{y}" x2="842" y2="{y}" stroke="#0e1628" stroke-width="3" opacity="0.7"/>')
    a(f'<g transform="rotate({tilt} 790 800)">')
    # head (facing left toward her)
    a('<path d="M690,690 L760,650 L860,660 L885,720 L870,790 L800,830 L740,820 L700,790 L640,780 L630,752 Z" fill="url(#chrome)" stroke="#0e1628" stroke-width="4" stroke-linejoin="round"/>')
    a('<path d="M630,752 L640,780 L700,790 L705,770 Z" fill="#15223a"/>')
    a('<path d="M632,748 L620,758 L632,770 Z" fill="#0b1220"/>')
    # ears
    a(f'<g transform="rotate({-14 if tilt else 0} 790 655)">')
    a('<path d="M770,655 L790,525 L825,650 Z" fill="url(#chrome)" stroke="#0e1628" stroke-width="4" stroke-linejoin="round"/>')
    a('</g>')
    a('<path d="M820,660 L865,540 L870,690 Z" fill="url(#chrome2)" stroke="#0e1628" stroke-width="4" stroke-linejoin="round"/>')
    a('<path d="M785,560 L800,640 M852,580 L858,660" stroke="#55c8ff" stroke-width="3" opacity="0.6"/>')
    # panel lines
    a('<path d="M700,720 L780,700 L860,710 M745,760 L800,800" stroke="#0e1628" stroke-width="3" fill="none" opacity="0.8"/>')
    # eye glow
    a('<circle cx="755" cy="712" r="34" fill="url(#glow)"/><ellipse cx="755" cy="712" rx="11" ry="8" fill="#e9f8ff"/>')
    a('<circle cx="845" cy="740" r="22" fill="#15223a" stroke="#9fb4cf" stroke-width="4"/><circle cx="845" cy="740" r="8" fill="#55c8ff"/>')
    a('</g>')
    a('</g>')
