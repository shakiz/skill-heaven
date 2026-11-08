import React from 'react';
import {
  AbsoluteFill, Sequence, Audio, Img, staticFile, useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from 'remotion';
import { loadFont } from '@remotion/google-fonts/Inter';

const { fontFamily } = loadFont('normal', { weights: ['400', '600', '700', '800'], subsets: ['latin'] });

export const FPS = 30;
export const DURATION = 55 * FPS; // 1650 frames

const C = {
  navy: '#14213D', panel: '#1B2A4D', line: '#2A3B63', amber: '#FCA311', white: '#FFFFFF',
  grey: '#C9D3E6', dim: '#8C9AB8', green: '#2EB872', red: '#E5484D', ink: '#14213D',
};
const MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace';
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const easeOut = Easing.out(Easing.cubic);

const useWide = () => {
  const { width, height } = useVideoConfig();
  return width > height;
};

// Fade + rise in, starting at `delay` frames.
const useAppear = (delay = 0, rise = 24) => {
  const f = useCurrentFrame() - delay;
  return {
    opacity: interpolate(f, [0, 14], [0, 1], { ...clamp, easing: easeOut }),
    transform: `translateY(${interpolate(f, [0, 18], [rise, 0], { ...clamp, easing: easeOut })}px)`,
  };
};

const Appear = ({ delay = 0, rise, style, children }) => {
  const a = useAppear(delay, rise);
  return <div style={{ ...style, ...a, transform: `${a.transform} ${style?.transform || ''}` }}>{children}</div>;
};

// Scene wrapper: fades the whole scene in and out.
const Scene = ({ dur, children, padding = 96 }) => {
  const f = useCurrentFrame();
  const opacity = interpolate(f, [0, 12, dur - 12, dur], [0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{ opacity, padding, fontFamily, color: C.white, display: 'flex', flexDirection: 'column' }}>
      {children}
    </AbsoluteFill>
  );
};

const Caption = ({ children, size, delay = 0, style }) => {
  const wide = useWide();
  return (
    <Appear delay={delay} style={{ fontSize: size || (wide ? 76 : 64), fontWeight: 800, lineHeight: 1.12, letterSpacing: -1, ...style }}>
      {children}
    </Appear>
  );
};

const A = ({ children }) => <span style={{ color: C.amber }}>{children}</span>;

/* ---------- icons (flat, single colour) ---------- */
const Icon = ({ name, size = 56, color = C.amber }) => {
  const p = { fill: 'none', stroke: color, strokeWidth: 2.2, strokeLinecap: 'round', strokeLinejoin: 'round' };
  const paths = {
    copy: <><rect x="8" y="8" width="13" height="13" rx="2" {...p} /><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3" {...p} /></>,
    warn: <><path d="M12 3 2 21h20L12 3z" {...p} /><path d="M12 10v5M12 18v.01" {...p} /></>,
    bot: <><rect x="4" y="7" width="16" height="12" rx="3" {...p} /><path d="M12 3v4M9 12v1M15 12v1M9 16h6" {...p} /></>,
    shield: <><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3z" {...p} /><path d="m8.5 12 2.5 2.5 4.5-5" {...p} /></>,
    list: <><path d="m4 6 1.5 1.5L8 5M4 12l1.5 1.5L8 11M4 18l1.5 1.5L8 17" {...p} /><path d="M11 6h9M11 12h9M11 18h9" {...p} /></>,
    file: <><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5z" {...p} /><path d="M14 3v5h5M9 13h6M9 17h6" {...p} /></>,
    lock: <><rect x="5" y="11" width="14" height="10" rx="2" {...p} /><path d="M8 11V7a4 4 0 0 1 8 0v4" {...p} /></>,
    doc: <><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5z" {...p} /><path d="M14 3v5h5" {...p} /></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24">{paths[name]}</svg>;
};

/* ---------- 1. Hook ---------- */
const Hook = ({ dur }) => {
  const f = useCurrentFrame();
  const wide = useWide();
  const pages = [0, 1, 2, 3, 4, 5, 6];
  const handDeg = interpolate(f, [0, dur], [0, 300]);
  return (
    <Scene dur={dur}>
      <div style={{ flex: 1, display: 'flex', flexDirection: wide ? 'row' : 'column', alignItems: 'center', justifyContent: 'space-between', gap: 48 }}>
        <div style={{ flex: 1 }}>
          <Caption delay={8}>Another 80-page RFP.</Caption>
          <Caption delay={40} style={{ marginTop: 12 }}><A>Due Friday.</A></Caption>
        </div>
        <div style={{ position: 'relative', width: wide ? 640 : 760, height: wide ? 600 : 470 }}>
          {pages.map((i) => {
            const s = spring({ frame: f - 6 - i * 7, fps: FPS, config: { damping: 200 } });
            return (
              <div key={i} style={{
                position: 'absolute', left: (wide ? 70 : 150) + i * 14, top: (wide ? 70 : 20) + i * 12, width: 300, height: 390,
                background: C.white, borderRadius: 12, boxShadow: '0 0 0 1px rgba(20,33,61,0.15)',
                opacity: s, transform: `translateY(${(1 - s) * -160}px) rotate(${(i % 2 ? 1 : -1) * (2 + i * 0.4)}deg)`,
                padding: 28, display: 'flex', flexDirection: 'column', gap: 14,
              }}>
                {[220, 180, 240, 160, 210, 120].map((w, k) => (
                  <div key={k} style={{ height: 12, width: w, borderRadius: 6, background: k === 0 ? C.ink : C.grey }} />
                ))}
              </div>
            );
          })}
          <div style={{
            position: 'absolute', right: wide ? 0 : 60, bottom: wide ? 10 : 0, width: 190, height: 190, borderRadius: '50%',
            background: C.navy, border: `10px solid ${C.amber}`, ...useAppear(30),
          }}>
            {[...Array(12)].map((_, k) => (
              <div key={k} style={{ position: 'absolute', left: 82, top: 6, width: 6, height: 14, borderRadius: 3, background: C.grey,
                transformOrigin: '3px 79px', transform: `rotate(${k * 30}deg)` }} />
            ))}
            <div style={{ position: 'absolute', left: 81, top: 30, width: 8, height: 56, borderRadius: 4, background: C.white,
              transformOrigin: '4px 55px', transform: `rotate(${handDeg}deg)` }} />
            <div style={{ position: 'absolute', left: 79, top: 76, width: 12, height: 12, borderRadius: 6, background: C.amber }} />
          </div>
        </div>
      </div>
    </Scene>
  );
};

/* ---------- 2. Problem ---------- */
const PainRow = ({ icon, text, delay }) => {
  const wide = useWide();
  return (
    <Appear delay={delay} style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
      <div style={{ width: 96, height: 96, borderRadius: 20, background: C.panel, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Icon name={icon} size={52} />
      </div>
      <div style={{ fontSize: wide ? 46 : 42, fontWeight: 700, lineHeight: 1.15 }}>{text}</div>
    </Appear>
  );
};

const Problem = ({ dur }) => {
  const f = useCurrentFrame();
  const wide = useWide();
  const strike = interpolate(f, [200, 235], [0, 100], { ...clamp, easing: easeOut });
  const red = interpolate(f, [200, 220], [0, 1], clamp);
  return (
    <Scene dur={dur}>
      <div style={{ flex: 1, display: 'flex', flexDirection: wide ? 'row' : 'column', gap: wide ? 80 : 56, alignItems: wide ? 'center' : 'stretch', justifyContent: 'center' }}>
        <div style={{ flex: wide ? 1.1 : 'none', display: 'flex', flexDirection: 'column', gap: 40 }}>
          <PainRow icon="copy" text="Copy-pasting answers from old proposals" delay={8} />
          <PainRow icon="warn" text={<>One missed “must” = <A>disqualified</A></>} delay={68} />
          <PainRow icon="bot" text="AI that promises 24/7 support you don’t offer" delay={128} />
        </div>
        <Appear delay={165} style={{ flex: wide ? 1 : 'none' }}>
          <div style={{ background: C.panel, borderRadius: 24, padding: 40, border: `3px solid ${red > 0.5 ? C.red : C.line}` }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14, fontSize: 26, color: C.dim, fontWeight: 600, marginBottom: 18 }}>
              <Icon name="bot" size={34} color={C.dim} /> Generic AI draft
            </div>
            <div style={{ fontSize: wide ? 42 : 38, fontWeight: 600, lineHeight: 1.3 }}>
              <span style={{
                backgroundImage: `linear-gradient(${C.red}, ${C.red})`, backgroundRepeat: 'no-repeat',
                backgroundSize: `${strike}% 6px`, backgroundPosition: '0 58%',
                boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone',
              }}>“We confirm 24/7 support with a 30-minute response time.”</span>
            </div>
            <div style={{ marginTop: 22, fontSize: 30, fontWeight: 700, color: C.red, opacity: red }}>
              Your company doesn’t offer that.
            </div>
          </div>
        </Appear>
      </div>
    </Scene>
  );
};

/* ---------- 3. Solution ---------- */
const Solution = ({ dur }) => {
  const f = useCurrentFrame();
  const wide = useWide();
  const s = spring({ frame: f - 4, fps: FPS, config: { damping: 200 } });
  return (
    <Scene dur={dur}>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', gap: 44 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 32, opacity: s, transform: `scale(${0.85 + 0.15 * s})` }}>
          <Img src={staticFile('logo.svg')} style={{ width: 180, height: 180 }} />
          <div style={{ fontSize: 120, fontWeight: 800, letterSpacing: -3 }}>BidReady</div>
        </div>
        <div>
          <Caption delay={30} size={wide ? 58 : 52}>{wide ? 'Turns any RFP into a submission-ready response,' : <>Turns any RFP into a<br />submission&#8209;ready response,</>}</Caption>
          <Caption delay={45} size={wide ? 58 : 52} style={{ marginTop: 8 }}>from <A>your own approved content.</A></Caption>
        </div>
      </div>
    </Scene>
  );
};

/* ---------- 4. How it works ---------- */
const StepTitle = ({ n, children }) => {
  const wide = useWide();
  return (
    <Appear delay={4} style={{ display: 'flex', alignItems: 'center', gap: 24, marginBottom: 44 }}>
      <div style={{ width: 76, height: 76, borderRadius: 38, background: C.amber, color: C.navy, fontSize: 42, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>{n}</div>
      <div style={{ fontSize: wide ? 60 : 50, fontWeight: 800, letterSpacing: -1, lineHeight: 1.1 }}>{children}</div>
    </Appear>
  );
};

const Chip = ({ color, children, solid, size = 24 }) => (
  <span style={{
    display: 'inline-block', padding: '6px 18px', borderRadius: 999, fontSize: size, fontWeight: 700,
    color: solid ? C.navy : color, background: solid ? color : 'transparent', border: `2px solid ${color}`, whiteSpace: 'nowrap',
  }}>{children}</span>
);

const LIB = [
  ['CO-001', 'Company overview (size, locations, history)', 'conflict'],
  ['CO-CERT-001', 'ISO/IEC 27001:2022 certification'],
  ['ANS-SUP-001', 'Support hours and incident response times (SLA)'],
  ['CS-001', 'Aarvik Municipality - citizen self-service portal'],
  ['PRC-001', 'Hourly rate card 2026 (EUR)'],
  ['PRC-INT-001', 'Discount authority and risk buffer', 'internal'],
];

const StepLibrary = ({ dur }) => {
  const wide = useWide();
  const f = useCurrentFrame();
  const conflict = interpolate(f, [118, 132], [0, 1], clamp);
  return (
    <Scene dur={dur}>
      <StepTitle n="1">Build your library from past proposals</StepTitle>
      <div style={{ flex: 1, display: 'flex', gap: 40, alignItems: 'flex-start' }}>
        {wide && (
          <div style={{ width: 420, display: 'flex', flexDirection: 'column', gap: 20, paddingTop: 40 }}>
            {['2024-03 Proposal - Odense Harbour.docx', '2026-05 Proposal - Ribe Water.docx'].map((t, i) => (
              <Appear key={t} delay={14 + i * 10} style={{ display: 'flex', gap: 16, alignItems: 'center', background: C.panel, borderRadius: 16, padding: '20px 22px' }}>
                <Icon name="doc" size={40} color={C.grey} />
                <div style={{ fontSize: 24, fontWeight: 600, color: C.grey, lineHeight: 1.25 }}>{t}</div>
              </Appear>
            ))}
            <Appear delay={34} style={{ fontSize: 64, color: C.amber, textAlign: 'center', fontWeight: 800 }}>→</Appear>
          </div>
        )}
        <Appear delay={wide ? 38 : 14} style={{ flex: 1, background: C.panel, borderRadius: 24, padding: wide ? '28px 36px' : '24px 28px' }}>
          <div style={{ fontFamily: MONO, fontSize: 24, color: C.dim, marginBottom: 14 }}>rfp-library/{wide ? '' : '  ← 2 past proposals'}</div>
          {LIB.map(([id, title, flag], i) => (
            <Appear key={id} delay={(wide ? 46 : 22) + i * 11} rise={14} style={{ padding: '14px 0', borderTop: i ? `1px solid ${C.line}` : 'none' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 20, flexWrap: 'wrap' }}>
                <span style={{ fontFamily: MONO, fontSize: 26, fontWeight: 700, color: C.amber, width: wide ? 210 : 190 }}>{id}</span>
                <span style={{ fontSize: wide ? 28 : 25, fontWeight: 600, flex: 1, minWidth: 0 }}>{title}</span>
                {flag === 'internal' && <Chip color={C.dim}>internal-only</Chip>}
              </div>
              {flag === 'conflict' && (
                <div style={{ marginTop: 10, marginLeft: wide ? 230 : 0, opacity: conflict, transform: `translateX(${(1 - conflict) * 20}px)` }}>
                  <Chip color={C.amber} solid>Conflict resolved: 120 → 140 employees</Chip>
                </div>
              )}
            </Appear>
          ))}
        </Appear>
      </div>
    </Scene>
  );
};

const ROWS = [
  ['3.1', 'ISO/IEC 27001 certification', 'Answered'],
  ['3.2', 'Liability insurance of at least EUR 5M', 'Answered'],
  ['3.4', 'Personal data stored in the EU/EEA', 'Answered'],
  ['3.5', 'Three public-sector references, with contacts', 'Gap'],
  ['4.6c', '30-minute response for critical incidents', 'Partial'],
  ['4.7a', 'On-site two days per week', 'Gap'],
];
const STATUS = { Answered: C.green, Partial: C.amber, Gap: C.red };

const StepMatrix = ({ dur }) => {
  const wide = useWide();
  const f = useCurrentFrame();
  const pulse = f > 100 ? 0.12 + 0.12 * (0.5 - 0.5 * Math.cos(((f - 100) / 26) * Math.PI)) : 0;
  return (
    <Scene dur={dur}>
      <StepTitle n="2">Every requirement tracked</StepTitle>
      <Appear delay={12} style={{ background: C.panel, borderRadius: 24, padding: wide ? '20px 36px' : '16px 24px' }}>
        <div style={{ display: 'flex', fontSize: 22, color: C.dim, fontWeight: 700, padding: '10px 0', letterSpacing: 1 }}>
          <div style={{ width: wide ? 130 : 96 }}>ID</div><div style={{ flex: 1 }}>REQUIREMENT</div><div style={{ width: 170, textAlign: 'right' }}>STATUS</div>
        </div>
        {ROWS.map(([id, text, st], i) => {
          const d = 22 + i * 10;
          const x = interpolate(f - d, [0, 16], [-40, 0], { ...clamp, easing: easeOut });
          const o = interpolate(f - d, [0, 12], [0, 1], clamp);
          const hot = id === '3.5';
          return (
            <div key={id} style={{
              display: 'flex', alignItems: 'center', padding: wide ? '24px 12px' : '24px 10px', margin: '0 -12px', borderRadius: 12,
              borderTop: `1px solid ${C.line}`, opacity: o, transform: `translateX(${x}px)`,
              background: hot ? `rgba(229,72,77,${pulse})` : 'transparent',
            }}>
              <div style={{ width: wide ? 130 : 96, fontFamily: MONO, fontSize: wide ? 32 : 26, fontWeight: 700, color: C.grey }}>{id}</div>
              <div style={{ flex: 1, fontSize: wide ? 36 : 28, fontWeight: 600, paddingRight: 16 }}>{text}</div>
              <div style={{ width: 170, textAlign: 'right' }}><Chip color={STATUS[st]} solid={st !== 'Answered'}>{st}</Chip></div>
            </div>
          );
        })}
      </Appear>
    </Scene>
  );
};

const StepProposal = ({ dur }) => {
  const wide = useWide();
  const f = useCurrentFrame();
  const scroll = interpolate(f, [40, 105], [0, wide ? -196 : -196], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const hl = interpolate(f, [112, 128], [0, 1], clamp);
  const bar = (w) => <div style={{ height: 14, width: w, borderRadius: 7, background: '#DCE2EE', margin: '12px 0' }} />;
  return (
    <Scene dur={dur}>
      <StepTitle n="3">Honest, ready-to-review proposal</StepTitle>
      <Appear delay={12} style={{ flex: 1, display: 'flex', justifyContent: 'center', overflow: 'hidden' }}>
        <div style={{ width: wide ? 1240 : 888, background: C.white, borderRadius: '16px 16px 0 0', color: C.ink, padding: wide ? '44px 64px' : '36px 40px', overflow: 'hidden' }}>
          <div style={{ transform: `translateY(${scroll}px)` }}>
            <div style={{ fontSize: 30, fontWeight: 800 }}>4.6a Describe your support and maintenance offering.</div>
            {bar('92%')}{bar('86%')}{bar('95%')}{bar('60%')}
            <div style={{ height: 30 }} />
            <div style={{ fontSize: 30, fontWeight: 800 }}>4.6c Response time of 30 minutes for critical incidents</div>
            <div style={{ fontSize: 24, fontStyle: 'italic', color: '#5B6785', margin: '10px 0 14px' }}>
              The municipality requires a response time of 30 minutes for critical incidents.
            </div>
            <div style={{ fontSize: 26, marginBottom: 14 }}><b>Compliance:</b> Exception - see response</div>
            <div style={{ fontSize: wide ? 29 : 26, lineHeight: 1.5 }}>
              Exception. Our committed response time for critical (P1) incidents is <b>1 hour, not the 30 minutes requested.</b> We state this openly rather than commit to a level we have not proven.{' '}
              <span style={{ background: `rgba(255,214,10,${0.95 * hl})`, fontWeight: 700, boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone', padding: '0 4px' }}>
                [VERIFY: Head of support to confirm whether a 30-minute P1 response can be offered]
              </span>
            </div>
            <div style={{ height: 34 }} />
            <div style={{ fontSize: 30, fontWeight: 800 }}>4.7a On-site presence at Vestby town hall</div>
            <div style={{ fontSize: 26, margin: '10px 0' }}><b>Compliance:</b> Exception - see response</div>
            {bar('94%')}{bar('88%')}{bar('91%')}{bar('64%')}{bar('85%')}{bar('72%')}
          </div>
        </div>
      </Appear>
    </Scene>
  );
};

/* ---------- 5. Benefits ---------- */
const BENEFITS = [
  ['shield', 'Never invents facts'],
  ['list', 'Never misses a requirement'],
  ['file', 'Real Word & Excel files'],
  ['lock', 'Private: your content stays in your folder'],
];

const Benefits = ({ dur }) => {
  const wide = useWide();
  return (
    <Scene dur={dur}>
      <Caption delay={4} style={{ marginBottom: 48 }}>Why <A>BidReady</A></Caption>
      <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, alignContent: 'center' }}>
        {BENEFITS.map(([icon, text], i) => (
          <Appear key={text} delay={20 + i * 28} style={{ background: C.panel, borderRadius: 24, padding: wide ? '40px 44px' : '32px 30px', display: 'flex', flexDirection: 'column', gap: 22, minHeight: wide ? 250 : 270 }}>
            <Icon name={icon} size={wide ? 64 : 56} />
            <div style={{ fontSize: wide ? 44 : 38, fontWeight: 800, lineHeight: 1.15 }}>{text}</div>
          </Appear>
        ))}
      </div>
    </Scene>
  );
};

/* ---------- 6. CTA ---------- */
const CTA = ({ dur }) => {
  const f = useCurrentFrame();
  const wide = useWide();
  const s = spring({ frame: f - 4, fps: FPS, config: { damping: 200 } });
  const out = interpolate(f, [dur - 10, dur], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ fontFamily, color: C.white, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 36, textAlign: 'center', opacity: Math.min(interpolate(f, [0, 12], [0, 1], clamp), out) }}>
      <Img src={staticFile('logo.svg')} style={{ width: 200, height: 200, opacity: s, transform: `scale(${0.88 + 0.12 * s})` }} />
      <Caption delay={14} size={wide ? 72 : 60}>BidReady. Available on <A>Agensi</A></Caption>
      <Caption delay={30} size={wide ? 48 : 42} style={{ fontWeight: 600, color: C.grey }}>Bid with confidence.</Caption>
    </AbsoluteFill>
  );
};

/* ---------- timeline ---------- */
const SCENES = [
  [Hook, 150], [Problem, 300], [Solution, 150],
  [StepLibrary, 200], [StepMatrix, 200], [StepProposal, 200],
  [Benefits, 300], [CTA, 150],
];

export const BidReadyVideo = () => {
  let from = 0;
  return (
    <AbsoluteFill style={{ background: C.navy }}>
      <Audio src={staticFile('music.wav')} volume={(f) => interpolate(f, [0, 45, DURATION - 60, DURATION], [0, 0.6, 0.6, 0], clamp)} />
      {SCENES.map(([Comp, dur], i) => {
        const el = (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <Comp dur={dur} />
          </Sequence>
        );
        from += dur;
        return el;
      })}
    </AbsoluteFill>
  );
};
