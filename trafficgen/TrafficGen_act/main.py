from drivingforce.TrafficTranformer.utils.arg_parse import get_parsed_args
from l5kit.configs import load_config_data
from utils.train import Trainer
from drivingforce.TrafficFormerDynamic.load_for_metadrive import AgentType,RoadEdgeType,RoadLineType
# ============================== Main =======================================
if __name__ == "__main__":
    # ===== parse args =====
    args = get_parsed_args()
    cfg = load_config_data(f'cfg/{args.cfg}.yaml')
    trainer = Trainer(exp_name=args.exp_name,
                      cfg=cfg,
                      args=args)
    cfg['device'] = 'cpu'

    trainer.load_model('/Users/fenglan/model_20.pt','cpu')
    #trainer.draw_showcase()
    trainer.draw_gifs()
    #trainer.generate_case_for_metadrive('/Users/fenglan/select')
    #trainer.eval_model()
    #trainer.train()
