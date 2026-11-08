import React from 'react';
import {
  AbsoluteFill, Sequence, Audio, Img, staticFile, useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from 'remotion';
import { loadFont } from '@remotion/google-fonts/Inter';

const { fontFamily } = loadFont('normal', { weights: ['400', '600', '700', '800'], subsets: ['latin'] });

export const FPS = 30;

const C = {
  navy: '#14213D', panel: '#1B2A4D', line: '#2A3B63', red: '#E63946', redText: '#FF6B74', white: '#FFFFFF',
  grey: '#C9D3E6', dim: '#8C9AB8', green: '#2EB872', amber: '#FCA311', ink: '#14213D', track: '#C0262D',
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
const Scene = ({ dur, children, padding = 96, center }) => {
  const f = useCurrentFrame();
  const opacity = interpolate(f, [0, 12, dur - 12, dur], [0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{ opacity, padding, fontFamily, color: C.white, display: 'flex', flexDirection: 'column', justifyContent: center ? 'center' : 'flex-start' }}>
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

const R = ({ children }) => <span style={{ color: C.redText }}>{children}</span>;

/* ---------- icons (flat, single colour) ---------- */
const Icon = ({ name, size = 56, color = C.redText }) => {
  const p = { fill: 'none', stroke: color, strokeWidth: 2.2, strokeLinecap: 'round', strokeLinejoin: 'round' };
  const paths = {
    eye: <><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" {...p} /><circle cx="12" cy="12" r="3" {...p} /></>,
    coin: <><circle cx="12" cy="12" r="9" {...p} /><path d="M15 9.5c-.5-1-1.6-1.5-3-1.5-1.7 0-3 .8-3 2s1.3 1.7 3 2 3 .8 3 2-1.3 2-3 2c-1.4 0-2.5-.5-3-1.5M12 6v2M12 16v2" {...p} /></>,
    mail: <><rect x="3" y="5" width="18" height="14" rx="2" {...p} /><path d="m3 7 9 6 9-6" {...p} /></>,
    book: <><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5z" {...p} /><path d="M4 21a2 2 0 0 1 2-2h13v2H6M8 7h7M8 11h5" {...p} /></>,
    pen: <><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4L16.5 3.5z" {...p} /><path d="M14 6l3 3" {...p} /></>,
    lock: <><rect x="5" y="11" width="14" height="10" rx="2" {...p} /><path d="M8 11V7a4 4 0 0 1 8 0v4" {...p} /></>,
    search: <><circle cx="11" cy="11" r="7" {...p} /><path d="m20 20-4-4" {...p} /></>,
    doc: <><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5z" {...p} /><path d="M14 3v5h5" {...p} /></>,
    warn: <><path d="M12 3 2 21h20L12 3z" {...p} /><path d="M12 10v5M12 18v.01" {...p} /></>,
    comment: <><path d="M4 5h16v11H9l-5 4V5z" {...p} /><path d="M8 9h8M8 12h5" {...p} /></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24">{paths[name]}</svg>;
};

const Chip = ({ color, children, solid, size = 24 }) => (
  <span style={{
    display: 'inline-block', padding: '6px 18px', borderRadius: 999, fontSize: size, fontWeight: 700,
    color: solid ? C.navy : color, background: solid ? color : 'transparent', border: `2px solid ${color}`, whiteSpace: 'nowrap',
  }}>{children}</span>
);

/* ---------- 1. Hook ---------- */
const Hook = ({ dur }) => {
  const f = useCurrentFrame();
  const wide = useWide();
  const pages = [0, 1, 2, 3, 4];
  const sign = interpolate(f, [70, 110], [0, 1], { ...clamp, easing: easeOut });
  return (
    <Scene dur={dur}>
      <div style={{ flex: 1, display: 'flex', flexDirection: wide ? 'row' : 'column', alignItems: 'center', justifyContent: wide ? 'space-between' : 'center', gap: wide ? 48 : 40 }}>
        <div style={{ flex: wide ? 1 : 'none', alignSelf: wide ? 'center' : 'flex-start' }}>
          <Caption delay={8}>Another 14-page contract.</Caption>
          <Caption delay={38} style={{ marginTop: 12 }}><R>“Just sign by Friday.”</R></Caption>
        </div>
        <div style={{ position: 'relative', width: wide ? 620 : 760, height: wide ? 600 : 470 }}>
          {pages.map((i) => {
            const s = spring({ frame: f - 6 - i * 7, fps: FPS, config: { damping: 200 } });
            const last = i === pages.length - 1;
            return (
              <div key={i} style={{
                position: 'absolute', left: (wide ? 90 : 190) + i * 14, top: (wide ? 70 : 10) + i * 12, width: 320, height: 410,
                background: C.white, borderRadius: 12, boxShadow: '0 0 0 1px rgba(20,33,61,0.15)',
                opacity: s, transform: `translateY(${(1 - s) * -160}px) rotate(${(i % 2 ? 1 : -1) * (1.5 + i * 0.4)}deg)`,
                padding: 28, display: 'flex', flexDirection: 'column', gap: 14, color: C.ink,
              }}>
                <div style={{ fontSize: 20, fontWeight: 800, letterSpacing: 1 }}>MASTER SERVICES AGREEMENT</div>
                {[250, 230, 260, 200, 240, 150].map((w, k) => (
                  <div key={k} style={{ height: 11, width: w, borderRadius: 6, background: C.grey }} />
                ))}
                {last && (
                  <div style={{ marginTop: 'auto' }}>
                    <svg width="240" height="70" viewBox="0 0 240 70">
                      <path d="M8 50c20-30 30-40 38-30s-10 30 4 26 20-36 34-30-6 28 10 26 26-20 40-18 10 14 30 10 30-6 60-6"
                        fill="none" stroke={C.ink} strokeWidth="3" strokeLinecap="round" pathLength="1"
                        strokeDasharray="1" strokeDashoffset={1 - sign} />
                    </svg>
                    <div style={{ height: 2, background: C.ink, width: 260 }} />
                    <div style={{ fontSize: 16, color: '#5B6785', marginTop: 6 }}>Signature</div>
                  </div>
                )}
              </div>
            );
          })}
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
      <div style={{ width: wide ? 96 : 84, height: wide ? 96 : 84, borderRadius: 20, background: C.panel, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Icon name={icon} size={wide ? 52 : 46} />
      </div>
      <div style={{ fontSize: wide ? 46 : 38, fontWeight: 700, lineHeight: 1.15 }}>{text}</div>
    </Appear>
  );
};

const Problem = ({ dur }) => {
  const f = useCurrentFrame();
  const wide = useWide();
  const hl = interpolate(f, [175, 200], [0, 1], { ...clamp, easing: easeOut });
  return (
    <Scene dur={dur}>
      <div style={{ flex: 1, display: 'flex', flexDirection: wide ? 'row' : 'column', gap: wide ? 80 : 44, alignItems: wide ? 'center' : 'stretch', justifyContent: 'center' }}>
        <div style={{ flex: wide ? 1.05 : 'none', display: 'flex', flexDirection: 'column', gap: wide ? 40 : 28 }}>
          <PainRow icon="eye" text="Signing clauses you don’t fully understand" delay={8} />
          <PainRow icon="coin" text={<>Paying a lawyer to read a <R>routine NDA</R></>} delay={60} />
          <PainRow icon="mail" text="Arguing changes in long email threads" delay={112} />
        </div>
        <Appear delay={150} style={{ flex: wide ? 1 : 'none' }}>
          <div style={{ background: C.white, color: C.ink, borderRadius: 20, padding: wide ? 40 : 32, border: `4px solid ${hl > 0.5 ? C.red : C.white}` }}>
            <div style={{ fontSize: 22, color: '#5B6785', fontWeight: 700, letterSpacing: 1, marginBottom: 14 }}>CLAUSE 12.1 · PAGE 11</div>
            <div style={{ fontSize: wide ? 34 : 30, lineHeight: 1.45 }}>
              This Agreement renews automatically for{' '}
              <span style={{ background: `rgba(230,57,70,${0.22 * hl})`, boxShadow: `inset 0 -4px 0 rgba(230,57,70,${hl})` }}>successive three (3) year terms</span>{' '}
              unless notice is given{' '}
              <span style={{ background: `rgba(230,57,70,${0.22 * hl})`, boxShadow: `inset 0 -4px 0 rgba(230,57,70,${hl})` }}>180 days</span>{' '}
              before renewal.
            </div>
            <div style={{ marginTop: 20, fontSize: 30, fontWeight: 800, color: C.red, opacity: hl }}>
              Easy to miss. Expensive to sign.
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
        <div style={{ display: 'flex', alignItems: 'center', gap: wide ? 32 : 24, opacity: s, transform: `scale(${0.85 + 0.15 * s})` }}>
          <Img src={staticFile('logo.svg')} style={{ width: wide ? 180 : 140, height: wide ? 180 : 140 }} />
          <div style={{ fontSize: wide ? 120 : 92, fontWeight: 800, letterSpacing: -3 }}>RedlineReady</div>
        </div>
        <div>
          <Caption delay={26} size={wide ? 56 : 48}>{wide ? 'Reviews every contract against your own playbook,' : <>Reviews every contract<br />against your own playbook,</>}</Caption>
          <Caption delay={40} size={wide ? 56 : 48} style={{ marginTop: 8 }}>then <R>redlines it in Word.</R></Caption>
        </div>
      </div>
    </Scene>
  );
};

/* ---------- 4. How it works ---------- */
const StepTitle = ({ n, children }) => {
  const wide = useWide();
  return (
    <Appear delay={4} style={{ display: 'flex', alignItems: 'center', gap: 24, marginBottom: wide ? 44 : 36 }}>
      <div style={{ width: 76, height: 76, borderRadius: 38, background: C.red, color: C.white, fontSize: 42, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>{n}</div>
      <div style={{ fontSize: wide ? 60 : 48, fontWeight: 800, letterSpacing: -1, lineHeight: 1.1 }}>{children}</div>
    </Appear>
  );
};

const PLAYBOOK = [
  ['Limitation of liability', '12 months’ fees', '6 months’ fees', 'Uncapped for us'],
  ['Payment terms', 'Net 30', 'Net 45', 'Beyond Net 60'],
  ['Auto-renewal', '1-year terms', '2-year terms', 'Any 3-year lock-in'],
  ['Governing law', 'Our home state', 'Neutral venue', 'Their courts only'],
];

const StepPlaybook = ({ dur }) => {
  const wide = useWide();
  const f = useCurrentFrame();
  const lockOn = interpolate(f, [110, 124], [0, 1], clamp);
  const cell = (label, value, internal, i) => (
    <div style={{ flex: 1, minWidth: 0 }}>
      <div style={{ fontSize: wide ? 18 : 16, color: internal ? C.redText : C.dim, fontWeight: 700, letterSpacing: 1, display: 'flex', alignItems: 'center', gap: 6, opacity: internal ? 0.4 + 0.6 * lockOn : 1 }}>
        {internal && <Icon name="lock" size={wide ? 18 : 16} color={C.redText} />}{label}
      </div>
      <div style={{ fontSize: wide ? 28 : 23, fontWeight: 600, marginTop: 4 }}>{value}</div>
    </div>
  );
  return (
    <Scene dur={dur} center>
      <StepTitle n="1">Your playbook, your positions</StepTitle>
      <Appear delay={12} style={{ background: C.panel, borderRadius: 24, padding: wide ? '22px 36px' : '18px 26px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16, marginBottom: 8 }}>
          <div style={{ fontFamily: MONO, fontSize: wide ? 24 : 21, color: C.dim }}>contract-playbook/</div>
          <Chip color={C.green} size={wide ? 22 : 19}>Starter playbook included</Chip>
        </div>
        {PLAYBOOK.map(([topic, std, fb, walk], i) => (
          <Appear key={topic} delay={24 + i * 12} rise={14} style={{ padding: wide ? '16px 0' : '13px 0', borderTop: `1px solid ${C.line}` }}>
            <div style={{ fontSize: wide ? 30 : 26, fontWeight: 800, color: C.white, marginBottom: 8 }}>{topic}</div>
            <div style={{ display: 'flex', gap: wide ? 32 : 18 }}>
              {cell('STANDARD', std, false, i)}
              {cell('FALLBACK', fb, true, i)}
              {cell('WALK-AWAY', walk, true, i)}
            </div>
          </Appear>
        ))}
      </Appear>
      <Appear delay={118} style={{ marginTop: wide ? 22 : 18, fontSize: wide ? 30 : 26, fontWeight: 700, color: C.grey, display: 'flex', alignItems: 'center', gap: 12 }}>
        <Icon name="lock" size={wide ? 32 : 28} /> Fallbacks and walk-aways stay internal.
      </Appear>
    </Scene>
  );
};

const RISKS = [
  ['9.2', 'Limitation of liability: uncapped', 'High'],
  ['12.1', 'Auto-renewal: 3-year terms, 180 days’ notice', 'High'],
  ['5.3', 'Payment: Net 90', 'Medium'],
  ['7.1', 'Confidentiality: mutual, 3 years', 'Low'],
  ['—', 'Data protection terms', 'Missing'],
];
const RISK = { High: C.red, Medium: C.amber, Low: C.green, Missing: C.grey };

const StepReview = ({ dur }) => {
  const wide = useWide();
  const f = useCurrentFrame();
  const pulse = f > 100 ? 0.1 + 0.12 * (0.5 - 0.5 * Math.cos(((f - 100) / 26) * Math.PI)) : 0;
  return (
    <Scene dur={dur} center>
      <StepTitle n="2">Every clause risk-rated</StepTitle>
      <Appear delay={12} style={{ background: C.panel, borderRadius: 24, padding: wide ? '20px 36px' : '16px 24px' }}>
        <div style={{ display: 'flex', fontSize: wide ? 22 : 19, color: C.dim, fontWeight: 700, padding: '10px 0', letterSpacing: 1 }}>
          <div style={{ width: wide ? 130 : 90 }}>{wide ? 'CLAUSE' : 'NO.'}</div><div style={{ flex: 1 }}>{wide ? 'ISSUE · BRIGHTLOOM SOFTWARE MSA' : 'ISSUE'}</div><div style={{ width: wide ? 180 : 150, textAlign: 'right' }}>RISK</div>
        </div>
        {RISKS.map(([id, text, risk], i) => {
          const d = 22 + i * 10;
          const x = interpolate(f - d, [0, 16], [-40, 0], { ...clamp, easing: easeOut });
          const o = interpolate(f - d, [0, 12], [0, 1], clamp);
          const hot = id === '12.1';
          return (
            <div key={text} style={{
              display: 'flex', alignItems: 'center', padding: wide ? '22px 12px' : '20px 10px', margin: '0 -12px', borderRadius: 12,
              borderTop: `1px solid ${C.line}`, opacity: o, transform: `translateX(${x}px)`,
              background: hot ? `rgba(230,57,70,${pulse})` : 'transparent',
            }}>
              <div style={{ width: wide ? 130 : 90, flexShrink: 0, fontFamily: MONO, fontSize: wide ? 32 : 26, fontWeight: 700, color: C.grey }}>{id}</div>
              <div style={{ flex: 1, fontSize: wide ? 34 : 26, fontWeight: 600, paddingRight: 16, lineHeight: 1.2 }}>{text}</div>
              <div style={{ width: wide ? 180 : 150, flexShrink: 0, textAlign: 'right' }}><Chip color={RISK[risk]} solid={risk !== 'Low'} size={wide ? 24 : 21}>{risk}</Chip></div>
            </div>
          );
        })}
      </Appear>
      <Appear delay={96} style={{ marginTop: wide ? 22 : 18, fontSize: wide ? 30 : 25, fontWeight: 700, color: C.grey }}>
        Plain-English explanation and a recommended position for each.
      </Appear>
    </Scene>
  );
};

// Tracked-change helpers: a deletion is struck through, an insertion is underlined, both in the reviewer colour.
const Del = ({ p, children }) => (
  <span style={{ color: p > 0 ? C.track : 'inherit', textDecoration: p > 0 ? 'line-through' : 'none', textDecorationThickness: 3 }}>{children}</span>
);
const Ins = ({ p, children }) => (
  <span style={{ color: C.track, textDecoration: 'underline', textDecorationThickness: 3, textUnderlineOffset: 5, opacity: p, display: p > 0 ? 'inline' : 'none', marginLeft: 6 }}>{children}</span>
);

const StepRedline = ({ dur }) => {
  const wide = useWide();
  const f = useCurrentFrame();
  const d1 = f > 44 ? 1 : 0;
  const i1 = interpolate(f, [56, 68], [0, 1], clamp);
  const d2 = f > 80 ? 1 : 0;
  const i2 = interpolate(f, [92, 104], [0, 1], clamp);
  const cm = interpolate(f, [112, 128], [0, 1], { ...clamp, easing: easeOut });
  const fs = wide ? 34 : 27;
  const bar = (w) => <div style={{ height: 13, width: w, borderRadius: 7, background: '#DCE2EE', margin: '11px 0' }} />;
  const comment = (
    <div style={{
      width: wide ? 440 : 'auto', background: '#FFF4F4', color: C.ink, borderRadius: 12, borderLeft: `6px solid ${C.track}`,
      padding: wide ? '20px 22px' : '16px 20px', opacity: cm, transform: `translateX(${(1 - cm) * 30}px)`,
      boxShadow: '0 8px 24px rgba(0,0,0,0.25)', alignSelf: wide ? 'center' : 'stretch',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: wide ? 20 : 18, fontWeight: 800, color: C.track, marginBottom: 8 }}>
        <Icon name="comment" size={wide ? 24 : 22} color={C.track} /> Comment
      </div>
      <div style={{ fontSize: wide ? 23 : 21, lineHeight: 1.4 }}>
        We propose annual renewal with 30 days’ notice, which is standard for subscription services.
      </div>
    </div>
  );
  return (
    <Scene dur={dur} center>
      <StepTitle n="3">A real Word redline, ready to send</StepTitle>
      <Appear delay={12} style={{ display: 'flex', flexDirection: wide ? 'row' : 'column', gap: wide ? 28 : 18, justifyContent: 'center', alignItems: wide ? 'center' : 'stretch' }}>
        <div style={{ width: wide ? 1060 : 'auto', background: C.white, borderRadius: 16, color: C.ink, padding: wide ? '36px 56px' : '26px 32px', overflow: 'hidden', position: 'relative' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <div style={{ fontSize: wide ? 20 : 17, fontWeight: 700, color: '#5B6785', letterSpacing: 1 }}>BRIGHTLOOM_MSA_v3_redline.docx</div>
            <div style={{ fontSize: wide ? 18 : 15, fontWeight: 800, color: C.white, background: C.track, borderRadius: 6, padding: '4px 10px' }}>TRACK CHANGES: ON</div>
          </div>
          {wide && <>{bar('94%')}{bar('70%')}</>}
          <div style={{ fontSize: fs, fontWeight: 800, marginTop: wide ? 18 : 10 }}>12. Term and Renewal</div>
          <div style={{ fontSize: fs, lineHeight: 1.55, marginTop: 8 }}>
            12.1 This Agreement renews automatically for successive{' '}
            <Del p={d1}>three&nbsp;(3)</Del><Ins p={i1}>one&nbsp;(1)</Ins>{' '}
            year terms unless either party gives{' '}
            <Del p={d2}>one hundred eighty (180)</Del><Ins p={i2}>thirty&nbsp;(30)</Ins>{' '}
            days’ written notice.
          </div>
          {bar('90%')}{bar('76%')}{wide && bar('58%')}
        </div>
        {comment}
      </Appear>
    </Scene>
  );
};

/* ---------- 5. Silent-edit detection ---------- */
const SilentEdit = ({ dur }) => {
  const wide = useWide();
  const f = useCurrentFrame();
  const alert = interpolate(f, [70, 84], [0, 1], { ...clamp, easing: easeOut });
  const shake = f > 84 && f < 100 ? Math.sin((f - 84) * 1.6) * 6 * (1 - (f - 84) / 16) : 0;
  const stat = (n, label, d) => (
    <Appear delay={d} style={{ background: C.panel, borderRadius: 20, padding: wide ? '24px 30px' : '18px 24px', display: 'flex', alignItems: 'center', gap: 18, flex: wide ? 'none' : 1 }}>
      <div style={{ fontSize: wide ? 56 : 46, fontWeight: 800, color: C.white }}>{n}</div>
      <div style={{ fontSize: wide ? 28 : 24, fontWeight: 600, color: C.grey, lineHeight: 1.2 }}>{label}</div>
    </Appear>
  );
  return (
    <Scene dur={dur} center>
      <Caption delay={4} size={wide ? 64 : 50} style={{ marginBottom: wide ? 44 : 32 }}>
        They sent it back. <R>We check what they didn’t track.</R>
      </Caption>
      <div style={{ display: 'flex', flexDirection: wide ? 'row' : 'column', gap: wide ? 40 : 24, alignItems: wide ? 'center' : 'stretch' }}>
        <div style={{ display: 'flex', flexDirection: wide ? 'column' : 'row', gap: wide ? 20 : 18, width: wide ? 420 : 'auto' }}>
          {stat('4', 'tracked changes', 20)}
          {stat('2', 'comments', 32)}
        </div>
        <div style={{
          flex: wide ? 1 : 'none', background: C.white, color: C.ink, borderRadius: 20, padding: wide ? '30px 40px' : '24px 28px',
          border: `5px solid ${C.red}`, opacity: alert, transform: `translateX(${shake}px) scale(${0.96 + 0.04 * alert})`,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14, fontSize: wide ? 30 : 26, fontWeight: 800, color: C.track, marginBottom: 14 }}>
            <Icon name="warn" size={wide ? 40 : 34} color={C.track} /> Untracked edit found · Clause 9.2
          </div>
          {[
            ['YOUR VERSION (v3)', <>Liability is capped at <b>twelve (12) months’</b> fees.</>, false],
            ['THEIR RETURN (v4)', <>Liability is capped at <b style={{ color: C.track, background: '#FFE3E5', padding: '0 4px' }}>three (3) months’</b> fees.</>, true],
          ].map(([label, text, hot]) => (
            <div key={label} style={{ padding: wide ? '14px 0' : '12px 0', borderTop: '1px solid #E3E8F2' }}>
              <div style={{ fontSize: wide ? 18 : 16, fontWeight: 800, letterSpacing: 1, color: hot ? C.track : '#5B6785' }}>{label}</div>
              <div style={{ fontSize: wide ? 30 : 26, lineHeight: 1.4, marginTop: 4 }}>{text}</div>
            </div>
          ))}
          <div style={{ marginTop: 8, fontSize: wide ? 24 : 21, fontWeight: 700, color: '#5B6785' }}>
            No tracked change, no comment. Flagged for you anyway.
          </div>
        </div>
      </div>
    </Scene>
  );
};

/* ---------- 6. Benefits ---------- */
const BENEFITS = [
  ['book', 'Your playbook, your positions'],
  ['pen', 'Real tracked changes in Word'],
  ['lock', 'Your fallbacks never leak'],
  ['search', 'Catches silent, untracked edits'],
];

const Benefits = ({ dur }) => {
  const wide = useWide();
  return (
    <Scene dur={dur}>
      <Caption delay={4} style={{ marginBottom: wide ? 48 : 40 }}>Why <R>RedlineReady</R></Caption>
      <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: wide ? 32 : 24, alignContent: 'center' }}>
        {BENEFITS.map(([icon, text], i) => (
          <Appear key={text} delay={20 + i * 26} style={{ background: C.panel, borderRadius: 24, padding: wide ? '40px 44px' : '30px 28px', display: 'flex', flexDirection: 'column', gap: 22, minHeight: wide ? 250 : 260 }}>
            <Icon name={icon} size={wide ? 64 : 54} />
            <div style={{ fontSize: wide ? 44 : 36, fontWeight: 800, lineHeight: 1.15 }}>{text}</div>
          </Appear>
        ))}
      </div>
      <Appear delay={130} style={{ marginTop: wide ? 28 : 22, fontSize: wide ? 28 : 23, fontWeight: 600, color: C.dim, textAlign: 'center' }}>
        Private: no network calls. Your contracts stay in your folder.
      </Appear>
    </Scene>
  );
};

/* ---------- 7. CTA ---------- */
const CTA = ({ dur }) => {
  const f = useCurrentFrame();
  const wide = useWide();
  const s = spring({ frame: f - 4, fps: FPS, config: { damping: 200 } });
  const out = interpolate(f, [dur - 10, dur], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ fontFamily, color: C.white, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 36, textAlign: 'center', padding: 80, opacity: Math.min(interpolate(f, [0, 12], [0, 1], clamp), out) }}>
      <Img src={staticFile('logo.svg')} style={{ width: 200, height: 200, opacity: s, transform: `scale(${0.88 + 0.12 * s})` }} />
      <Caption delay={14} size={wide ? 72 : 56}>{wide ? <>RedlineReady. Available on <R>Agensi</R></> : <>RedlineReady.<br />Available on <R>Agensi</R></>}</Caption>
      <Caption delay={30} size={wide ? 48 : 40} style={{ fontWeight: 600, color: C.grey }}>Sign with confidence.</Caption>
      <Caption delay={44} size={wide ? 24 : 21} style={{ fontWeight: 500, color: C.dim, letterSpacing: 0 }}>A first-pass contract review, not legal advice.</Caption>
    </AbsoluteFill>
  );
};

/* ---------- timeline ---------- */
const SCENES = [
  [Hook, 135], [Problem, 240], [Solution, 120],
  [StepPlaybook, 180], [StepReview, 180], [StepRedline, 220],
  [SilentEdit, 190], [Benefits, 240], [CTA, 135],
];

export const DURATION = SCENES.reduce((a, [, d]) => a + d, 0); // 1640 frames, ~54.7 s

export const RedlineReadyVideo = () => {
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
