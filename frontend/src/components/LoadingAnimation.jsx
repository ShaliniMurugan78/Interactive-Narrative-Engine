import "./LoadingAnimation.css";

export default function LoadingAnimation({ message = "Loading..." }) {
  return (
    <div className="loading-screen">
      <div className="loading-inner">
        <div className="loading-orb">
          <div className="orb-ring ring1" />
          <div className="orb-ring ring2" />
          <div className="orb-ring ring3" />
          <div className="orb-core">✦</div>
        </div>
        <p className="loading-msg">{message}</p>
        <div className="loading-dots">
          <span /><span /><span />
        </div>
      </div>
    </div>
  );
}
