import { registerRoot, Composition } from 'remotion';
import { RedlineReadyVideo, FPS, DURATION } from './Video';

const Root = () => (
  <>
    <Composition id="Main" component={RedlineReadyVideo} durationInFrames={DURATION} fps={FPS} width={1920} height={1080} />
    <Composition id="Square" component={RedlineReadyVideo} durationInFrames={DURATION} fps={FPS} width={1080} height={1080} />
  </>
);

registerRoot(Root);
