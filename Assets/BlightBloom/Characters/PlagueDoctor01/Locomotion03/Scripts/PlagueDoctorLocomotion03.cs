using UnityEngine;
using BlightBloom.Traversal;

namespace BlightBloom.Characters
{
    /// <summary>Character-only in-place gait driver. Reads the existing player; never moves it.</summary>
    [DefaultExecutionOrder(100)]
    public sealed class PlagueDoctorLocomotion03 : MonoBehaviour
    {
        [SerializeField] private Animator animator;
        [SerializeField] private Transform leftThigh, leftShin, leftFoot, rightThigh, rightShin, rightFoot;
        [SerializeField] private Transform leftHeel, leftToe, rightHeel, rightToe;
        [SerializeField, Min(.1f)] private float walkCycleDistance = 1.4f, sprintCycleDistance = 2.5f;
        [SerializeField, Range(0f,1f)] private float groundContactWeight = 1f;
        private Transform player;
        private CharacterController controller;
        private TraversalInput input;
        private Vector3 previous;
        private float speed, previousYaw, turning;
        private int mode;
        private readonly Contact left = new Contact(), right = new Contact();
        private static readonly int Playback = Animator.StringToHash("Playback");
        private sealed class Contact { public bool planted; public Vector3 anchor; }
        public float VisualSpeed => speed;
        public string Gait => mode == 2 ? "Sprint" : mode == 1 ? "Walk" : "Idle";

        public void Configure(Animator source, Transform lt, Transform ls, Transform lf, Transform rt, Transform rs, Transform rf,
                              Transform lh, Transform lto, Transform rh, Transform rto)
        { animator=source; leftThigh=lt; leftShin=ls; leftFoot=lf; rightThigh=rt; rightShin=rs; rightFoot=rf;
          leftHeel=lh; leftToe=lto; rightHeel=rh; rightToe=rto; }
        private void OnEnable() => ResetOwner();
        private void ResetOwner()
        {
            player=transform.parent;
            if(player==null)return;
            controller=player.GetComponent<CharacterController>(); input=player.GetComponent<TraversalInput>();
            previous=player.position; previousYaw=player.eulerAngles.y; speed=0; mode=0;
            left.planted=right.planted=false;
            if(animator!=null)animator.applyRootMotion=false;
        }
        private void Update()
        {
            if(player==null)ResetOwner();
            if(player==null||animator==null)return;
            float dt=Mathf.Max(Time.deltaTime,.0001f);
            Vector3 delta=player.position-previous; delta.y=0; previous=player.position;
            float measured=delta.magnitude/dt;
            if(measured>12f){measured=0; left.planted=right.planted=false;}
            speed=Mathf.Lerp(speed,measured,1f-Mathf.Exp(-16f*dt));
            turning=Mathf.Lerp(turning,Mathf.Abs(Mathf.DeltaAngle(previousYaw,player.eulerAngles.y))/dt,1f-Mathf.Exp(-12f*dt));
            previousYaw=player.eulerAngles.y;
            int desired=speed>(mode==0?.18f:.12f)?(input!=null&&input.Sprint&&speed>2.5f?2:1):0;
            if(desired!=mode)
            {
                var state=animator.GetCurrentAnimatorStateInfo(0);
                float phase=mode==0?0:Mathf.Repeat(state.normalizedTime,1f);
                animator.CrossFadeInFixedTime(desired==2?"Sprint":desired==1?"Walk":"Idle",desired==0?.20f:.16f,0,phase);
                mode=desired; left.planted=right.planted=false;
            }
            animator.SetFloat(Playback, mode==0?1f:Mathf.Clamp(speed/(mode==2?sprintCycleDistance:walkCycleDistance),.15f,3.2f));
        }
        private void LateUpdate()
        {
            if(animator==null||controller==null)return;
            var state=animator.GetCurrentAnimatorStateInfo(0);
            bool moving=mode!=0; float phase=Mathf.Repeat(state.normalizedTime,1f);
            bool stable=!animator.IsInTransition(0);
            float duty=mode==2?.32f:.55f;
            float weight=controller.isGrounded?groundContactWeight:0;
            Solve(leftThigh,leftShin,leftFoot,leftHeel,leftToe,left,!moving||stable&&phase<duty,weight,moving);
            Solve(rightThigh,rightShin,rightFoot,rightHeel,rightToe,right,!moving||stable&&Mathf.Repeat(phase+.5f,1f)<duty,weight,moving);
        }
        private void Solve(Transform thigh,Transform shin,Transform foot,Transform heel,Transform toe,Contact contact,bool stance,float weight,bool moving)
        {
            if(thigh==null||shin==null||foot==null||heel==null||toe==null)return;
            Vector3 original=foot.position; Quaternion rotation=foot.rotation;
            bool found=false; RaycastHit best=default;
            foreach(var hit in Physics.RaycastAll(original+Vector3.up*.35f,Vector3.down,1.05f,~(1<<2),QueryTriggerInteraction.Ignore))
            {
                if(hit.transform==player||hit.transform.IsChildOf(player)||hit.normal.y<.5f)continue;
                if(!found||hit.distance<best.distance){best=hit;found=true;}
            }
            if(!found||weight<=0){contact.planted=false;return;}
            float sole=Mathf.Min(heel.position.y,toe.position.y);
            float correction=Mathf.Clamp(best.point.y+.007f-sole,-.08f,.16f);
            // Preserve authored flight and knee recovery. Only stance feet settle down to the surface.
            if(moving&&!stance)correction=Mathf.Max(0,correction);
            Vector3 target=original+Vector3.up*correction;
            if(stance&&moving&&turning<75)
            {
                if(!contact.planted){contact.anchor=target;contact.planted=true;}
                Vector3 offset=contact.anchor-target;offset.y=0;
                target+=Vector3.ClampMagnitude(offset,.065f);
            }
            else contact.planted=false;
            target=Vector3.Lerp(original,target,weight);
            Vector3 hip=thigh.position,kneeOriginal=shin.position;
            float upper=Vector3.Distance(hip,kneeOriginal),lower=Vector3.Distance(kneeOriginal,original);
            Vector3 axis=(target-hip).normalized;
            float distance=Mathf.Clamp(Vector3.Distance(hip,target),.03f,upper+lower-.001f);
            // Retain the authored knee plane instead of imposing a forward pole every frame.
            Vector3 pole=kneeOriginal-hip;pole-=axis*Vector3.Dot(pole,axis);
            if(pole.sqrMagnitude<.00001f)pole=Vector3.ProjectOnPlane(player.forward,axis);
            pole.Normalize();
            float along=(upper*upper-lower*lower+distance*distance)/(2*distance);
            Vector3 knee=hip+axis*along+pole*Mathf.Sqrt(Mathf.Max(0,upper*upper-along*along));
            thigh.rotation=Quaternion.FromToRotation(shin.position-hip,knee-hip)*thigh.rotation;
            shin.rotation=Quaternion.FromToRotation(foot.position-shin.position,target-shin.position)*shin.rotation;
            foot.rotation=rotation;
        }
    }
}
