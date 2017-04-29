

Ext.ux.EasyChangePass = Ext.extend(Ext.Panel, {

      // title: 'Change password'
      // ,iconCls: 'icon-key'
        border:false
        ,initComponent(...args) {
                                
                    this.form_change_pass = new Ext.FormPanel({
                      waitMsgTarget: true
                        ,labelAlign: 'right'
                        ,labelWidth: 150
                        ,disabled: false
                        ,border:false
                         
                        ,items: [
                            {
                                html:'Changement de votre mot de passe'
                                ,style:'margin:20px'
                                ,border:false
                            },
                
                            {
                            xtype:'textfield',
                            fieldLabel: 'mot de passe actuel',
                            inputType:'password',
                            name: 'current',
                            width:120
                            }
                            ,{
                            xtype:'textfield',
                            fieldLabel: 'nouveau mot de passe',
                            inputType:'password',
                            name: 'new1',
                            width:120
                            }
                            ,{
                            xtype:'textfield',
                            fieldLabel: 'confirmation',
                            inputType:'password',
                            name: 'new2',
                            width:120
                            } 
                            , {
                            xtype:'button'
                            ,text:'changer le mot de passe'
                            ,iconCls:'icon-disk'
                            ,style:'margin-top:20px;margin-left:auto;margin-right:auto'
                            ,listeners: {
                                scope:this
                                ,'click': {
                                    fn(button, e) {
                                        var formpanel = button.findParentByType('form');
                                        var form = formpanel.getForm();
                                        form.el.mask('Loading...');
                                        form.submit({
                                             url: '/apps/login/changepassword'
                                            ,method: 'POST'
                                            ,scope: this
                                            ,success(form, action) { 
                                                Ext.Msg.alert("Success", "Le mot de passe a été changé avec succès");  
                                                console.log(this);
                                                this.fireEvent('submitSuccess');
                                                }
                                            ,failure(form, action) {  form.el.unmask(); Ext.Msg.alert("Failure", action.result.msg);}
                                                });
                                            }   
                                        }
                                        }
                            }
                           ]
                        
                                
                         })
                            this.form_change_pass
                          this.items = this.form_change_pass;
 
              // Ext.apply(this, {
                    // layout:'fit'
                    // ,items:this.form_change_pass
                      // })

            Ext.ux.EasyChangePass.superclass.initComponent.apply(this, args);
            
             this.addEvents(['submitSuccess']);
            }
        
 
}); 

// register xtype



Ext.reg('EasyChangePass', Ext.ux.EasyChangePass); 





